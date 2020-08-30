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
* Getting work code
CREATE OR REPLACE FUNCTION get_tasks()
RETURNS TABLE (market_hash_name text, game_app_id integer, price_action text)
AS $$
DECLARE
    _market_hash_name text;
    _game_app_id integer;
    _price_action text;
BEGIN
    FOR _market_hash_name, _game_app_id, _price_action IN SELECT item, app_id, action
                                                          FROM task
                                                          WHERE (timeout_time IS NULL OR timeout_time <= timezone('utc', now()))
                                                          AND action != 'Live Price'
                                                          GROUP BY item, app_id, action
                                                          ORDER BY min(due_date)
                                                          LIMIT 50
    LOOP
        UPDATE task
        SET timeout_time=(timezone('utc', now()) + INTERVAL '0.25 DAY')::timestamp
        WHERE item=_market_hash_name AND app_id=_game_app_id AND action=_price_action;

        market_hash_name := _market_hash_name;
        game_app_id := _game_app_id;
        price_action := _price_action;

        RETURN NEXT;
    END LOOP;
    RETURN;
END;
$$ LANGUAGE plpgsql;
