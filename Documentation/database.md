# Steam Data
## Table Structure
* CREATE TABLE IF NOT EXISTS public.PriceLive(market_hash_name text NOT NULL PRIMARY KEY, time timestamp NOT NULL PRIMARY KEY, sell_price numeric(8, 3), buy_price numeric(8, 3), median_price numeric(8, 3), volume integer, sell_quantity integer, buy_quantity integer, total_sell_quantity integer, total_buy_quantity integer)
* CREATE TABLE IF NOT EXISTS public.PriceHourly(market_hash_name text NOT NULL PRIMARY KEY REFERENCES Item(market_hash_name), time timestamp NOT NULL PRIMARY KEY, median_price numeric(8, 3), volume integer)
* CREATE TABLE IF NOT EXISTS public.PriceDaily(market_hash_name text NOT NULL PRIMARY KEY REFERENCES Item(market_hash_name), time timestamp NOT NULL PRIMARY KEY, median_price numeric(8, 3), volume integer)
* CREATE TABLE IF NOT EXISTS public.Item(market_hash_name text NOT NULL PRIMARY KEY, name text, app_id integer REFERENCES Game(app_id), icon text)
* CREATE TABLE IF NOT EXISTS public.Game(app_id integer NOT NULL PRIMARY KEY, name text, icon text)
* CREATE TABLE IF NOT EXISTS public.CsgoItem(market_hash_name text NOT NULL PRIMARY KEY REFERENCES Item(market_hash_name), collection text, classification text, item_type text)

# Tasks To Do
## Table Structure
* CREATE TABLE public.task(item text REFERENCES public."Item"(market_hash_name), app_id integer NOT NULL REFERENCES public."Game"(app_id), action text NOT NULL, due_date timestamp NOT NULL, timeout_time timestamp, PRIMARY KEY(item, app_id, action))
* Operation Phoenix Weapon Case's market_hash_name is used for game scans

## Workers
* CREATE TABLE workers (name text NOT NULL, ip text NOT NULL, last_ping timestamp NOT NULL, process_id integer NOT NULL, PRIMARY KEY(name, ip, last_ping));
