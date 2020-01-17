# Scraper Library
* Before use, make sure cookie is valid which generally means changing it every day to a new cookie
* The API is able to find the number of items a game has, get the basic details of items in the game (name, icon URL) and get the price history of items (date, median price, volume)

# Steam API
* Using a web scraper to obtain the data required through Steam's json files
* Item names are obtained through the template https://steamcommunity.com/market/search/render/?start={}&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&appid={}&norender=1&count=100
* All price history is obtained through the template https://steamcommunity.com/market/pricehistory/?country=AU&currency=3&appid={}&market_hash_name={}
* Today's price history is obtained through the template https://steamcommunity.com/market/priceoverview/?appid={}&market_hash_name={}&currency=3

# Steam's Item URLs
* Steam has some unique cases for items where it is abnormal
* An incorrect case is item "PGC 2019 - M416"'s string which is "PGC%C2%A02019%20-%20M416" which can be seen as PGC = PGC, " " = %C2%A0, "2019" = "2019", " " = "%20, "-" = "-", " " = "%20", "M416" = "M416" and hence https://steamcommunity.com/market/pricehistory/?country=AU&currency=1&appid=578080&market_hash_name=PGC%C2%A02019%20-%20M416 is the correct URL while https://steamcommunity.com/market/pricehistory/?country=AU&currency=1&appid=578080&market_hash_name=PGC 2019 - M416 is wrong even though it isn't being taken up by another item
* A correct case is "Shattered Web Case" which is "Shattered%20Web%20Case" which makes sense as the " " changes into "%20" and hence, https://steamcommunity.com/market/pricehistory/?country=AU&currency=1&appid=730&market_hash_name=Shattered%20Web%20Case is the correct URL along with https://steamcommunity.com/market/pricehistory/?country=AU&currency=1&appid=730&market_hash_name=Shattered Web Case
* Currently, the edge cases are being ignored

# Price History
* Median price can be a nonstandard financial number such as 3.245 but that is due to currency conversion

# Initial/Update Scrape
* Each scrape will obtain all item names currently on the market and obtain the corresponding price history for the items
* The functions in the API are dynamic and will add onto or create a new file and hence, every time the application is ran, the latest data is obtained

# Avoid Blocking
* The website can be indexed at most 20 times a minute per page
* Our function to get the page (get_page()) does not sleep but rather spam the server as frequently as possible and if it does block, we wait it out till we are unblocked but we still send a request every 3 seconds
* We are able to continuously spam as their servers have a maximum of 20 requests a minute rather than banning style of service control
* We chose 3 seconds as the per minute cap is reset at approximately the 20th second of every minute and hence, we generally do not need to wait a whole minute before the next set of requests
