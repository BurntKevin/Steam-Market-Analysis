#!/bin/sh

# Resetting code to latest version
git reset --hard
git pull

# Cleaning up from previous scrape
rm reporting_stack.txt
rm output.txt
rm steam_scraper_activity.txt
rm steam_scraper_data.txt
rm steam_scraper_stack.txt

# Starting scrape
nohup python3 steam_scraper.py &
