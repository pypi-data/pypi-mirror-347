#import pytest
from bifsg import BIFSG

def bifsg_test():
    obj = BIFSG(census_api_key="dummy", one_line_address="", surname="", firstname="Nancy")
    result = obj.BIFSG_predict()
    return result

if __name__ == "__main__":
    # Run the test
    result = bifsg_test()
    print(result)



