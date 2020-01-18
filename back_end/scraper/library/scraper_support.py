"""
Scraper generic functions
COOKIE to access logged in only information
data_to_pickle_file saves data
data_from_pickle_file loads data
get_page gets page information
"""
# Support Functions
from pickle import load, dump # Save data
from json import loads # Get information from website
from time import sleep # Controls amount of requests being sent to website
from requests import get # Connect to website

# Cookie to access login only information: pricehistory
COOKIE = {"steamLoginSecure": "76561198362858068%7C%7C4A7F799705D1E223CFB7FB9D271185D67451AE59"}

def list_duplicate_remover(given_list):
    """
    Removes duplicates from a list while maintaining order where the first
    instance is kept
    """
    return list(dict.fromkeys(given_list))

def data_to_pickle_file(data, file_location):
    """
    Saves data into a pickle file
    """
    with open(file_location, "wb") as file:
        dump(data, file)

def data_from_pickle_file(file_location):
    """
    Obtains data from a pickle file
    """
    return load(open(file_location, "rb"))

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
    string = string.replace("$", "%24")

    return string

def get_file_location(game_id):
    """
    Returns the file location for a game
    """
    return "../../data/{}_items.txt".format(game_id)
