"""
Obtain's sentiment from various IG Trading assets and stores it into a database

Obtain's data about the price of an asset (bid/ask) along with trader's sentiment and the current date
Scrapes page every 15 minutes (has a buffer with of 1 minute + 5 seconds for each URL)
Database is designed to store: source, asset class, date, percentage long, buy price, sell price
Generic URL: https://www.ig.com/au/{asset_class}/markets-{asset_class}/{asset}
"""
import datetime
from time import sleep
from bs4 import BeautifulSoup
from requests import get
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, NUMERIC, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creating database table if required
BASE = declarative_base()

class Sentiment(BASE):
    """
    Used to store sentiment of a commodity from a website
    """
    __tablename__ = "Sentiment"

    source = Column(String, primary_key=True)
    asset = Column(String, primary_key=True)
    date = Column(DateTime, primary_key=True)
    percentage_long = Column(Integer)
    sell = Column(NUMERIC)
    buy = Column(NUMERIC)

DB = create_engine("sqlite:///sentiment.db")
SESSION = sessionmaker(DB)
SESSION = SESSION()
BASE.metadata.create_all(DB)

# Scraper class
class Scraper:
    """
    Used to scrape websites for information
    """
    def __init__(self, ig_markets_urls):
        """
        URLs to scrape from
        """
        self.ig_markets_urls = ig_markets_urls
    def ig_markets_scrape_sentiment(self):
        """
        Scrapes sentiment from IG Markets and stores it into Sentiment database
        """
        def clean_ig_markets_sentiment_page(page):
            """
            Cleans IG Market's sentiment page
            """
            # Obtaining percentage which are long/short
            percentage = page.find("span", class_="price-ticket__percent")
            percentage = percentage.text
            percentage = percentage[:-1]

            # Obtaining current majority position
            position = page.find("div", class_="price-ticket__sentiment")
            position = page.find("strong")
            position = position.text

            # Obtaining buy price
            buy = page.find("a", class_="price-ticket__button price-ticket__button--buy")
            buy = buy.find("div", class_="price-ticket__price")
            buy = buy.text

            # Obtaining sell price
            sell = page.find("a", class_="price-ticket__button price-ticket__button--sell")
            sell = sell.find("div", class_="price-ticket__price")
            sell = sell.text

            return (percentage, position, buy, sell)

        while True:
            # For all URLs
            for url in self.ig_markets_urls:
                # Obtaining web page
                response = get(url)
                soup = BeautifulSoup(response.text, "html.parser")

                # Obtaining time of web page
                date = datetime.datetime.now()

                # Obtaining information about the page
                percentage, position, buy, sell = clean_ig_markets_sentiment_page(soup)

                # Standardising data to a long position
                if position == "short":
                    percentage = 100 - int(percentage)

                # Adding to database
                self.add_sentiment_entry("IG Markets", url.split("/")[-1], date, percentage, buy, sell)

                # To minimise DDOS
                sleep(1)

            # Add completion time for each iteration
            print(datetime.datetime.now())

            # Obtaining latest data every 15 minutes with a buffer for URL size
            sleep(14 * 60 - 5 * len(self.ig_markets_urls))
    def add_sentiment_entry(self, source, asset, date, percentage_long, buy, sell):
        """
        Adding new entry to sentiment database
        """
        try:
            # Creating database session
            database_connection = sessionmaker(create_engine("sqlite:///sentiment.db"))

            # Creating entry
            entry = Sentiment(source=source, asset=asset, percentage_long=percentage_long, sell=sell, buy=buy, date=date)

            # Adding entry to database
            con = database_connection()
            con.add(entry)
            con.commit()
        except:
            # Unsuccessful add
            print("!", end="")
            with open(f"sentiment_scraper_crash_report_{source}.txt", "a") as file:
                file.write(f"Failed: {source}, {asset}, {date}, {percentage_long}, {buy}, {sell}\n")
        else:
            # Signal successful scrape
            print(".", end="")

if __name__ == "__main__":
    SCRAPER = Scraper(
        [
            "https://www.ig.com/au/indices/markets-indices/australia-200",
            "https://www.ig.com/au/forex/markets-forex/bitcoin-1",
            "https://www.ig.com/au/forex/markets-forex/aud-usd",
            "https://www.ig.com/au/commodities/markets-commodities/gold",
            "https://www.ig.com/au/commodities/markets-commodities/brent-crude",
            "https://www.ig.com/au/forex/markets-forex/eur-usd",
            "https://www.ig.com/au/indices/markets-indices/wall-street",
            "https://www.ig.com/au/indices/markets-indices/us-spx-500"
        ]
    )

    SCRAPER.ig_markets_scrape_sentiment()
