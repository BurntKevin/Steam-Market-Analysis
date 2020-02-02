# Scraper Library
* Before use, make sure cookie is valid which generally means changing it every day to a new cookie
* The API is able to find the number of items a game has, get the basic details of items in the game (name, icon URL) and get the price history of items (date, median price, volume)

# Steam API
* Using a web scraper to obtain the data required through Steam's json files
* Item count is obtained from https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=100&appid={}&start=0
* Item names are obtained through the template https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&norender=1&count=100&appid={}&start={}
* All price history is obtained through the template https://steamcommunity.com/market/pricehistory/?appid={}&market_hash_name={}

# Steam's Item URLs
* Steam has some unique cases for items where it is abnormal
* An incorrect case is item "PGC 2019 - M416"'s string which is "PGC%C2%A02019%20-%20M416" which can be seen as PGC = PGC, " " = %C2%A0, "2019" = "2019", " " = "%20, "-" = "-", " " = "%20", "M416" = "M416" and hence https://steamcommunity.com/market/pricehistory/?country=AU&currency=1&appid=578080&market_hash_name=PGC%C2%A02019%20-%20M416 is the correct URL while https://steamcommunity.com/market/pricehistory/?country=AU&currency=1&appid=578080&market_hash_name=PGC 2019 - M416 is wrong even though it isn't being taken up by another item
* A correct case is "Shattered Web Case" which is "Shattered%20Web%20Case" which makes sense as the " " changes into "%20" and hence, https://steamcommunity.com/market/pricehistory/?country=AU&currency=1&appid=730&market_hash_name=Shattered%20Web%20Case is the correct URL along with https://steamcommunity.com/market/pricehistory/?country=AU&currency=1&appid=730&market_hash_name=Shattered Web Case
* Currently, these edge cases are being ignored

# Price History
* Median price can be a nonstandard financial number such as 3.245 but that is due to currency conversion

# Initial/Update Scrape
* Each scrape will obtain all item names currently on the market and obtain the corresponding price history for the items
* The functions in the API are dynamic and will add onto or create a new item and hence, every time the application is ran, the latest data is obtained for all items of a game

# Avoid Blocking
* The website can be indexed at most 20 times a minute per page
* Our function to get the page (get_page) does not sleep but rather spam the server as frequently as possible and if it does block, we wait it out till we are unblocked but we still send a request every 3 seconds while we wait
* We are able to continuously send requests as their servers have a maximum of 20 requests a minute rather than bannning if requests are too frequent
* We chose 3 seconds as the per minute cap is reset at approximately the 20th second of every minute and hence, we generally do not need to wait a whole minute before the next set of requests

# Analysis
* Analyses the prices with RSI and MACD

# Issues with Technical Analysis
* Some items do not have a high turnover where they are rarely sold which causes issues in analysis methods
* For example, RSI requires data points to be surrounding a particular point in order for a calculation to be resulted, however, some items will have them blank which results in partial RSI lines drawn for the chart
