"""
Runs steam_scraper.py
"""
# Obtaining request from user
from sys import argv

# Library used to scrape
from steam_scraper import SteamScraper

# Monitoring tools
from reporting import print_issue, send_email

# Checking arguments given by user
if len(argv) != 2 or not (argv[1] == "new" or argv[1] == "update" or argv[1] == "live"):
    print_issue("Incorrect usage of scraper, only one argument (new, update or live)")
    exit(1)

# Creating Scraper
SCRAPER = SteamScraper()
while True:
    if argv[1] == "new":
        # Cosntantly scan for new items
        SCRAPER.scan_for_new_items("730")
    elif argv[1] == "update":
        # Constantly scan for new official prices
        SCRAPER.scan_for_new_official_prices()
    elif argv[1] == "live":
        # Constantly scan for new live prices
        SCRAPER.scan_for_live_prices()
    else:
        print_issue("Could not understand command {argv[1]}")
        break

    send_email(f"Finished a round of scanning for {argv[1]}")
