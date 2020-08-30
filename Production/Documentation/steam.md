# Steam Data
## Data Format
* Price is in USD
* Times are in UTC

# Links
## Obtain Items
* https://steamcommunity.com/market/search/render/?count=100&norender=1&appid={app_id}&start={start}

## Price History
* API: https://steamcommunity.com/market/pricehistory/?appid={app_id}&market_hash_name={market_hash_name}
* Scrape: https://steamcommunity.com/market/listings/{app_id}/{market_hash_name}
* For one month ago, it contains 1 hour per point
* For more than one month ago, it contains 1 day per point

## Current Situation of Market
* Obtain current instant buy price and sell price along with volume and median price of hour
* https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item_name_id}}
* API (Best Instant Buy, Best Instant Sell, Pending Orders): https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={item_name_id}}
* API (Used for Last 24 Hour Volume): https://steamcommunity.com/market/priceoverview/?appid={app_id}&market_hash_name={market_hash_name}

## Obtain All Games
* http://api.steampowered.com/ISteamApps/GetAppList/v0002

# Issues to Consider
* No available price: Some items have no volume or prices beyond the Steam Market's price limit
