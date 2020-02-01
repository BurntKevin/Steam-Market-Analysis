"""
Scraper generic functions
"""
# Support Functions
from json import loads # Get information from website
from time import sleep # Controls amount of requests being sent to website
from requests import get # Connect to website

# Cookie to access login only information: price history
COOKIE = {"steamLoginSecure": "76561198362858068%7C%7CDEA5F0380E19EA0017601852D4A9389EAA4AB285"}

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

    return string

def get_game_name_from_id(game_id):
    """
    Obtainins a game's name from it's game id
    """
    # Obtaining game names and game ids
    game_data = get_page("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    game_data = game_data["applist"]["apps"]

    # Locating game with corresponding game_id
    for game in game_data:
        if game["appid"] == game_id:
            # Game found
            return game["name"]

    # Game id does not exist
    return None

# TODO: Release when doing technical analysis
# def fill_price(price_history):
#     # Obtaining all possible dates
#     dates = []
#     # If there is no price history, no need to find all dates
#     if len(price_history) != 0:
#         # Calculating points between dates
#         start = price_history[0]["price_history_point_date"]
#         end = datetime.datetime.today()

#         # Generating points
#         while start <= end:
#             dates.append(sc_pricehistorypoint(start, None, 0, None, None).deobject())
#             start += datetime.timedelta(days=1)

#     # Sorting
#     all_dates = dates + price_history
#     all_dates = merge_sort_price_history(all_dates)

#     # Returning data
#     return all_dates
