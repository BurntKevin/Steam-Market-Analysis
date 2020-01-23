"""
Testing scraper_support functions
"""
# Support functions
from time import sleep # Used as we need to become blocked by the website
from requests import get # Used to get blocked by the website

# Library to be tested
from scraper_support import get_page, string_to_query_string

def test_get_page():
    """
    Test get_page
    Tested normal request, request when blocked
    """
    # Variable
    url = "https://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name=StatTrak%E2%84%A2%20M4A1-S%20|%20Hyper%20Beast%20(Minimal%20Wear)"

    # Testing successful request after being blocked
    # Getting blocked
    while get(url).status_code == 200:
        continue
    # Ensuring that the function gets the success
    page = get_page(url)
    assert page["success"]

    # Testing normal successful request
    sleep(60)
    page = get_page(url)
    assert page["success"]

def test_string_to_query_string():
    """
    Test string_to_query_string
    Tested normal string, $
    """
    # Standard Conversions
    assert string_to_query_string(" ") == "%20"
    assert string_to_query_string("$") == "%24"
    assert string_to_query_string("|") == "%7C"
    assert string_to_query_string("(") == "%28"
    assert string_to_query_string(")") == "%29"

    # Items
    assert string_to_query_string("Shattered Web Case") == "Shattered%20Web%20Case"
    assert string_to_query_string("5$") == "5%24"
    assert string_to_query_string("MAC-10 | Surfwood (Factory New)") == "MAC-10%20%7C%20Surfwood%20%28Factory%20New%29"
    assert string_to_query_string("Mann Co. Supply Crate Key") == "Mann%20Co.%20Supply%20Crate%20Key"
    assert string_to_query_string("FAMAS | Crypsis (Field-Tested)") == "FAMAS%20%7C%20Crypsis%20%28Field-Tested%29"

test_string_to_query_string()
