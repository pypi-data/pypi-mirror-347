# bifsg/data_prep.py
import os
import requests
import json
import yaml
import pandas as pd
import numpy as np

from importlib import resources

# (1) National population
def nat_population(api_key: str) -> dict:
    url = (
        "https://api.census.gov/data/2020/dec/dp"
        f"?get=NAME,DP1_0092C,DP1_0093C,DP1_0104C,DP1_0105C,"
        "DP1_0106C,DP1_0107C,DP1_0108C,DP1_0109C,DP1_0110C,DP1_0111C"
        "&for=us:*"
        f"&key={api_key}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    headers, rows = data[0], data[1:]
    return dict(zip(headers, rows[0]))

# (2) Surnames cleaning
def surnames_cleaning(input_path: str) -> pd.DataFrame:
    df = pd.read_excel(input_path, sheet_name="2010 Census Names")
    cols = ['pcthispanic','pctwhite','pctblack','pctaian','pctapi','pct2prace']
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce") / 100

    df['subtotal'] = 1 - df[cols].sum(axis=1, skipna=True)
    df['count_nan'] = df[cols].isna().sum(axis=1)

    def impute(row):
        if row['count_nan'] > 0:
            fill = row['subtotal'] / row['count_nan']
            for c in cols:
                if pd.isna(row[c]):
                    row[c] = fill
        return row

    df = df.apply(impute, axis=1)

    # convert pct→counts (adding 0.01 for zeros), then recompute pct
    for race in ['hispanic','white','black','api','aian','2prace']:
        pctcol = f"pct{race}"
        df[race] = np.where(df[pctcol]==0, 0.01, df[pctcol]*df['count'])
    df['total'] = df[['hispanic','white','black','api','aian','2prace']].sum(axis=1)
    for race in ['hispanic','white','black','api','aian','2prace']:
        df[f"pct{race}"] = df[race] / df['total']

    return df

# (3) First-names cleaning
def firstnames_cleaning(input_path: str) -> pd.DataFrame:
    fn = pd.read_excel(input_path, sheet_name="Data")
    # obs * pct → counts
    for race in ['hispanic','white','black','api','aian','2prace']:
        fn[race] = (0.01 * fn['obs'] * fn[f"pct{race}"]).round().astype(int)
        fn[race] = np.where(fn[race]==0, 0.01, fn[race])

    # recompute pct → fraction
    for race in ['hispanic','white','black','aian','api','2prace']:
        fn[f"pct{race}"] /= 100

    # totals
    totals = {f"total_{race}": fn[race].sum() for race in ['hispanic','white','black','api','aian','2prace']}
    for col, val in totals.items():
        fn[col] = val

    # race given firstname
    mat = fn[['hispanic','white','black','aian','api','2prace']].values
    denom = fn[[f"total_{race}" for race in ['hispanic','white','black','aian','api','2prace']]].values
    p_f_r = mat / denom
    p_f_r = pd.DataFrame(p_f_r,
                         columns=[f"fn_g_r_{race}" for race in ['hispanic','white','black','aian','api','2prace']])
    return pd.concat([fn, p_f_r], axis=1)

def main():
    # ensure data folder exists
    pkg_dir = os.path.dirname(__file__)
    data_dir = os.path.join(pkg_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # (1) nat_population.yaml
    nat = nat_population(os.environ.get("CENSUS_API_KEY", ""))  # fallback to env var
    with open(os.path.join(data_dir, "nat_population.yaml"), "w") as f:
        yaml.dump({"nat_population": nat}, f)
    print("→ nat_population.yaml written")

    # (2) surnames_updated.parquet
    surn = surnames_cleaning(os.path.join(data_dir, "Names_2010Census.xlsx"))
    surn.to_parquet(os.path.join(data_dir, "surnames_updated.parquet"))
    print("→ surnames_updated.parquet written")

    # (3) firstnames_updated.parquet
    fn = firstnames_cleaning(os.path.join(data_dir, "firstnames.xlsx"))
    fn.to_parquet(os.path.join(data_dir, "firstnames_updated.parquet"))
    print("→ firstnames_updated.parquet written")

if __name__ == "__main__":
    main()
