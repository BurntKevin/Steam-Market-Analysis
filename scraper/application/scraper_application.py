"""
Application takes in an infinite amount of arguments to create its associated
price history
"""
# Support functions
import sys # Access API and to take in argumetns

# Importing scraping API
sys.path.insert(0, "../library")
from scraper import get_items_price_history

# Obtaining number of games are inputted
ARGUMENTS = len(sys.argv)

# Informing user how to correctly use the application
if ARGUMENTS == 1:
    print("Usage: python scraper_application {game_ids}")

# Scrapping the data required
for i in range(1, ARGUMENTS):
    # Updating user of progress
    print("Currently scraping game {}".format(sys.argv[i]))

    # Scraping data
    game = get_items_price_history(sys.argv[i])

    # Saving game
    game.save()
