"""
Scraper generic functions
COOKIE to access logged in only information
get_page gets page information
"""
# Support Functions
from json import loads # Get information from website
from time import sleep # Controls amount of requests being sent to website
from requests import get # Connect to website

# Cookie to access login only information: pricehistory
COOKIE = {"steamLoginSecure": "76561198362858068%7C%7C8F457EEA131799F3762C909704FEE9510B754D2A"}

def get_page(url):
    """
    Obtains data about a game and waits until unblocked if blocked
    """
    # Obtaining page
    page = get(url, cookies=COOKIE)

    # Informing user of status
    print("URL {} has status code {}".format(url, page.status_code))

    if page.status_code != 200:
        # Unsuccessfully obtained page, retrying in 3 seconds
        sleep(3)
        return get_page(url)

    # Successfully obtained page, returning page
    page = page.content
    page = loads(page)
    return page

def string_to_query_string(string):
    """
    Extra formatting to a string before being used as query string
    May not include all required transformations and this does not do automatic
    string conversions such as " " to "%20"
    """
    string = string.replace(" ", "%20")
    string = string.replace("$", "%24")
    string = string.replace("|", "%7C")
    string = string.replace("(", "%28")
    string = string.replace(")", "%29")

    return string
