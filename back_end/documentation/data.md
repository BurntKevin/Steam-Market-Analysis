# Data
* Stores the data obtained from scraper - games, items belonging to games and price history for items

# Connector
* Turns scraper data objects into database records
* Turns database records into scraper data objects

# Excessive Data
* A lot of data can be removed such as storing turnover which can be calculated on the spot. However, in favour of faster search times, we are not opting to dynamically calculate the information but rather simply query it. Especially since in every instance, we are going to require the information such as turnover. Hence, we are storing all data statically.
