"""
Testing scraper_support functions
"""
# Support functions
from os.path import exists # Check if a directory exists
from os import remove # Remove files
from time import sleep # Used as we need to become blocked by the website
import sys # Allows use of library
from requests import get # Used to get blocked by the website

# Library to be tested
sys.path.insert(0, "../library")
from scraper_support import list_duplicate_remover, data_to_pickle_file, data_from_pickle_file, get_page, string_to_query_string, get_file_location

def test_list_duplicate_remover():
    """
    Test list_duplicate_remover
    Tested with a list with duplicates and a list without duplicates
    """
    # Variables
    duplicate_list = ["1", "2", "4", "4", "2", "5"]
    no_duplicate_list = ["1", "2", "4", "5"]

    # Testing list with duplicates
    assert list_duplicate_remover(duplicate_list) == no_duplicate_list

    # Testing list without duplicates
    assert list_duplicate_remover(duplicate_list) == no_duplicate_list

def test_data_to_pickle_file():
    """
    Test data_to_pickle_file
    Tested list
    """
    # Ensuring that tmp.txt does not already exist
    if exists("tmp.txt"):
        raise ValueError("tmp.txt exists, not overwriting")

    # Creating pickle file
    data = [1, 2, 3]
    data_to_pickle_file(data, "tmp.txt")

    # Reading data from pickle file
    data_obtained = data_from_pickle_file("tmp.txt")

    # Testing that the data is the same
    assert data == data_obtained

    # Cleaning up
    remove("tmp.txt")

def test_data_from_pickle_file():
    """
    Test data_from_pickle_file
    Tested list
    """
    # Ensuring that tmp.txt does not already exist
    if exists("tmp.txt"):
        raise ValueError("tmp.txt exists, not overwriting")

    # Creating pickle file
    data = [1, 2, 3]
    data_to_pickle_file(data, "tmp.txt")

    # Reading data from pickle file
    data_obtained = data_from_pickle_file("tmp.txt")

    # Testing that the data is the same
    assert data == data_obtained

    # Cleaning up
    remove("tmp.txt")

def test_get_page():
    """
    Test get_page
    Tested normal request, request when blocked
    """
    # Variable
    url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=USD&market_hash_name=StatTrak%E2%84%A2%20M4A1-S%20|%20Hyper%20Beast%20(Minimal%20Wear)"

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
    # Normal string
    assert string_to_query_string("Shattered Web Case") == "Shattered Web Case"

    # $ Sign
    assert string_to_query_string("5$") == "5%24"

def test_get_file_location():
    """
    Test get_file_location
    """
    # Testing function
    assert get_file_location("730") == "../../data/730_items.txt"

    # Ensuring function is not returning a single stagnant string
    assert get_file_location("123") == "../../data/123_items.txt"
