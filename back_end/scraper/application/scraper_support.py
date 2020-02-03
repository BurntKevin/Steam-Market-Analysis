"""
Scraper generic functions
"""
# Support Functions
from json import loads # Get information from website
from time import sleep # Controls amount of requests being sent to website
from requests import get # Connect to website

# Cookie to access login only information: price history
COOKIE = {"steamLoginSecure": "76561198362858068%7C%7CF4A50A618EA2B004ABAEFBEF17587EB816790409"}

def get_page(url, try_number=0):
    """
    Obtains data about a game and waits until unblocked if blocked
    Tries for a maximum of 60 times (3 block iterations) to deal with
    inaccessible situations such as an incorrectly formatted url so that the
    request can continue rather than stop
    """
    # If trying exceeds 3 minutes (60 tries), give up
    if try_number == 60:
        print("Failed {}".format(url))
        return None

    # Obtaining page
    page = get(url, cookies=COOKIE)

    # Informing user of status
    print("URL {} has status code {}".format(url, page.status_code))

    if page.status_code != 200:
        # Unsuccessfully obtained page, retrying in 3 seconds
        sleep(3)
        return get_page(url, try_number + 1)

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
    string = string.replace("&", "%26")

    return string

def get_game_name_from_id(game_id):
    """
    Obtains a game's name from it's game id
    """
    # Obtaining game names and game ids
    game_data = get_page("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    game_data = game_data["applist"]["apps"]

    # Locating game with corresponding game_id
    for game in game_data:
        if str(game["appid"]) == str(game_id):
            # Game found
            return game["name"]

    # Game id does not exist
    return None

def sort_objects_by_date(objects):
    """
    Sorts an object with a date variable in an ascending date order
    """
    if len(objects) > 1:
        middle = len(objects) // 2 # Finding the middle of the list
        L = objects[:middle] # Dividing the list elements
        R = objects[middle:] # into 2 halves

        # Partitioning the sorting
        sort_objects_by_date(L) # Sorting the first half
        sort_objects_by_date(R) # Sorting the second half

        i = j = k = 0
        # Copy data to temporary list L[] and R[]
        while i < len(L) and j < len(R):
            if L[i].date < R[j].date:
                objects[k] = L[i]
                i += 1
            else: 
                objects[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            objects[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            objects[k] = R[j]
            j += 1
            k += 1

    return objects
