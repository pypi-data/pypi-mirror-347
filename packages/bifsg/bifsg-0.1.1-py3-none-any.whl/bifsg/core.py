import requests
import json
import yaml
import pandas as pd
import numpy as np
import os
from importlib import resources

class BIFSG:
    def __init__(
        self,
        census_api_key: str,
        one_line_address: str,
        surname: str,
        firstname: str,
    ):
        self.census_api_key = census_api_key
        self.one_line_address = one_line_address
        self.surname = surname.upper()
        self.firstname = firstname.upper()

        # load helper data
        with resources.path(__package__ + '.data', 'surnames_updated.parquet') as p:
            self.surnames = pd.read_parquet(p)
        with resources.path(__package__ + '.data', 'firstnames_updated.parquet') as p:
            self.firstnames = pd.read_parquet(p)

        # load national population
        with resources.open_text(__package__ + '.data', 'nat_population.yaml') as file:
            self.nat_population = yaml.safe_load(file)['nat_population']

    def _MatchAddress(self):
        census_geocode_url = f'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address={self.one_line_address}&benchmark=2020&vintage=2010&format=json'

        try:
            census_geocode_response = requests.get(census_geocode_url).json()
            try: 
                state = census_geocode_response['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['STATE']
                county = census_geocode_response['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['COUNTY']
                tract = census_geocode_response['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['TRACT']
                block = census_geocode_response['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['BLOCK']
                return [state, county, tract, block]
            except:
                try:
                    census_geocode_response['result']['addressMatches']
                    print("No address matched, using names only")
                    return None
                except:
                    print(census_geocode_response)
                    return None
        except (requests.exceptions.RequestException, ValueError) as err:
            print(f"An error occurred: {err}")
    

    def _GetCensusData(self):
        if self._MatchAddress():
            state, county, tract, block = self._MatchAddress()
            block = str(block).zfill(4)
            state = str(state).zfill(2)
            county = str(county).zfill(3)
            tract = str(tract).zfill(6)
            demographics_url = f'https://api.census.gov/data/2020/dec/pl?get=P2_001N,P2_002N,P2_003N,P2_004N,P2_005N,P2_006N,P2_007N,P2_008N,P2_009N,P2_010N,P2_011N&for=block:{block}&in=state:{state}&in=county:{county}&in=tract:{tract}&key={self.census_api_key}'
            try:
                response = requests.get(demographics_url).json()
                headers = response[0]
                data = response[1]
                return dict(zip(headers, data))
            except (requests.exceptions.RequestException, ValueError) as err:
                print(f"An error occurred: {err}")
        else:
            print("no census data matched, use only names")
            return None
    
    def _GetProb_cb_given_race(self):
        geocoderesult = self._GetCensusData()
        if geocoderesult:
            geocoderesult = {k:geocoderesult[k] for k in ['P2_002N','P2_005N','P2_006N','P2_007N','P2_008N','P2_009N','P2_010N','P2_011N']}
            if list(geocoderesult.values()) != ['0','0','0','0','0','0','0','0']:
                #add 0.01 to the zero observations and convert to numeric
                geocoderesult = {k: (float(v) + 0.01 if v == "0" else float(v)) for k, v in geocoderesult.items()}
                results = {}
                #calculate geo given race probability
                results['p_g_r_hispanic'] = geocoderesult['P2_002N']/int(self.nat_population['DP1_0105C'])
                results['p_g_r_white'] = geocoderesult['P2_005N']/int(self.nat_population['DP1_0105C'])
                results['p_g_r_black'] = geocoderesult['P2_006N']/int(self.nat_population['DP1_0106C'])
                results['p_g_r_aian'] = geocoderesult['P2_007N']/int(self.nat_population['DP1_0107C'])
                results['p_g_r_api'] = (geocoderesult['P2_008N']+geocoderesult['P2_009N'])/(int(self.nat_population['DP1_0108C'])+int(self.nat_population['DP1_0109C']))
                results['p_g_r_other'] = (geocoderesult['P2_010N']+geocoderesult['P2_011N'])/(int(self.nat_population['DP1_0110C'])+int(self.nat_population['DP1_0111C']))
                
                return results
            else:
                print("census block data unavailable")
                return {'p_g_r_hispanic':1,'p_g_r_white':1,'p_g_r_black':1,'p_g_r_aian':1,'p_g_r_api':1,'p_g_r_other':1}
        else:
            return {'p_g_r_hispanic':1,'p_g_r_white':1,'p_g_r_black':1,'p_g_r_aian':1,'p_g_r_api':1,'p_g_r_other':1}

    def _GetGeoProb(self):
        geocoderesult = self._GetCensusData()
        
        if geocoderesult:
            geocoderesult = {k:geocoderesult[k] for k in ['P2_002N','P2_005N','P2_006N','P2_007N','P2_008N','P2_009N','P2_010N','P2_011N']}
            if list(geocoderesult.values()) != ['0','0','0','0','0','0','0','0']:
                #add 0.01 to the zero observations and convert to numeric
                geocoderesult = {k: (float(v) + 0.01 if v == "0" else float(v)) for k, v in geocoderesult.items()}
            
                #calculate race given geo probability
                results = {}
                subtotal = geocoderesult['P2_002N']+geocoderesult['P2_005N']+geocoderesult['P2_006N']+ geocoderesult['P2_007N']+geocoderesult['P2_008N']+geocoderesult['P2_009N']+geocoderesult['P2_010N']+geocoderesult['P2_011N']
                results['pcthispanic'] = geocoderesult['P2_002N']/subtotal
                results['pctwhite'] = geocoderesult['P2_005N']/subtotal
                results['pctblack'] = geocoderesult['P2_006N']/subtotal
                results['pctaian'] = geocoderesult['P2_007N']/subtotal
                results['pctapi'] = (geocoderesult['P2_008N']+geocoderesult['P2_009N'])/subtotal
                results['pctother'] = (geocoderesult['P2_010N']+geocoderesult['P2_011N'])/subtotal
                
                return results
            else:
                print("census block data unavailable")
                return {'pcthispanic':1,'pctwhite':1,"pctblack":1,"pctaian":1,"pctapi":1,"pctother":1}
        else:
            return {'pcthispanic':1,'pctwhite':1,"pctblack":1,"pctaian":1,"pctapi":1,"pctother":1}
    

    def _GetSurnameProb(self):
        surname = self.surname.upper()
        keys = ['pcthispanic','pctwhite','pctblack','pctaian','pctapi','pct2prace']
        if not self.surnames.empty and surname in self.surnames['name'].values:
            surname_probs = self.surnames.loc[self.surnames['name']==surname,keys].iloc[0].tolist()
            return dict(zip(keys,surname_probs))
        else:
            return dict(zip(keys,[1,1,1,1,1,1]))
    
    #function to get race given firstname probabilities
    def _GetProb_firstname_given_race(self):
        firstname = self.firstname.upper()
        keys = ['fn_g_r_hispanic','fn_g_r_white','fn_g_r_black','fn_g_r_aian','fn_g_r_api','fn_g_r_2prace']
        if not self.firstnames.empty and firstname in self.firstnames['firstname'].values:
            firstname_probs = self.firstnames.loc[self.firstnames['firstname']==firstname,["fn_g_r_hispanic","fn_g_r_white","fn_g_r_black","fn_g_r_aian","fn_g_r_api","fn_g_r_2prace",]].iloc[0].tolist()
            return dict(zip(keys,firstname_probs))
        else:
            return dict(zip(keys,[1,1,1,1,1,1]))

    #functions to get race probabilities based on firstname
    def _Getfirstname_probs(self):
        firstname = self.firstname.upper()
        keys = ['pcthispanic','pctwhite','pctblack','pctaian','pctapi','pct2prace']
        if not self.firstnames.empty and firstname in self.firstnames['firstname'].values:
            firstname_probs = self.firstnames.loc[self.firstnames['firstname']==firstname,keys].iloc[0].tolist()
            return dict(zip(keys,firstname_probs))
        else:
            return dict(zip(keys,[1,1,1,1,1,1]))
        
    #aggregation function
    def BIFSG_predict(self):
        race_probs = []
        p_r_s = self._GetSurnameProb()
        p_f_g_r = self._GetProb_firstname_given_race()
        p_g_g_r = self._GetProb_cb_given_race()
        #If surname can be found in database, use Race Given Surname as prior, and Firstname Given Race & Geocode Given Race as posterior. If any or both of these two cannot be found, their corresponding values are assigned as 1 and won't affect outcome
        if list(p_r_s.values()) != [1,1,1,1,1,1]:
            print("Using Surname as prior")
            products = [x*y*z for x, y, z in zip(list(p_r_s.values()), 
                                                list(p_f_g_r.values()), list(p_g_g_r.values()))]
            sum_of_products = sum(products)
            final_values = [product / sum_of_products for product in products]
        else:
            #If surname cannot be found. Use Race Given Geocode as prior, and Firstname Given Race as posterior. If Firstname cannot be found, its values are assigned as 1 and won't affect outcome
            p_r_g = self._GetGeoProb()
            if list(p_r_g.values()) != [1,1,1,1,1,1]:
                print("Surname not in database, using Geocode as prior")
                products = [x*y for x, y in zip(list(p_f_g_r.values()), list(p_r_g.values()))]
                sum_of_products = sum(products)
                final_values = [product / sum_of_products for product in products]
            else:
                #if geocode cannot be found, use Race Given Firstname as outcome
                p_r_f = self._Getfirstname_probs()
                print(p_r_f)
                if list(p_r_f.values()) != [1,1,1,1,1,1]:
                    print("Surname not in database, using firstname only")
                    final_values = list(p_r_f.values())
                else:
                    #if all missing, give NA values.
                    print("All missing")
                    final_values = [None,None,None,None,None,None]
        return dict(zip(["hispanic","white","black","AIAN","API","Other"],final_values))
