"""
Database connector to store steam market data
"""
# Time checker
from datetime import datetime
from time import sleep
from dateutil import relativedelta

# Obtaining details about machine
from socket import gethostname, gethostbyname
from os import getpid

# Connecting to database
from psycopg2 import connect, OperationalError

# Multithreading
from threading import Thread

# Monitoring
from reporting import log_issue, send_email, print_issue

class SteamDatabase:
    """
    Connector to Steam Data Database
    """
    def __init__(self, admin=True):
        """
        Sets up connections to the database along with checks
        """
        # Management of commits
        self.queued_items = []

        # Connection to database
        if admin:
            # Requires low latency read and writes
            self.database = connect(host="steamdata.cpl2ejcsikco.us-east-1.rds.amazonaws.com", port="5432", database="postgres", user="steamdata_admin", password="egion=us-e4tsdggsdgast-f21#database:id=steam")
        else:
            # Only reading allowed
            self.database = connect(host="steamdataread.cpl2ejcsikco.us-east-1.rds.amazonaws.com", port="5432", database="postgres", user="postgres_ro", password="J%vYCPsbEVqd88wWJcM&FWuHb*26BjsLmXt*kgjNrN^Yv!n")
    def ping_database(self):
        """
        Inserts an entry to signal aliveness containing computer name, ip address and process id
        """
        # Sending a notification about the status of the machine
        self.queue_database(f"INSERT INTO workers (name, ip, last_ping, process_id) VALUES ('{gethostname()}', '{gethostbyname(gethostname())}', '{datetime.utcnow()}'::timestamp, {getpid()})")
        self.commit_checker()
    def shutdown(self):
        # Saving progress
        while self.queued_items:
            print_issue(f"Saving {self.queued_items}")
            self.commit()

        # Shutting down connection
        self.database.close()

        # Informing user
        print_issue("Successfully shut down database connection, may need to wait for commit to finish")
    def queue_database(self, entry):
        """
        Adds an item to the queue
        """
        self.queued_items.append(entry)
    def update_database(self, entries):
        """
        Executes commands to the database
        """
        def save_to_file(entries):
            """
            Saves all SQL statements into a file
            """
            for entry in entries:
                log_issue("steam_scraper_data", f"{entry};", date=False)
        # Checking if there are items to commit
        if entries:
            # Informing user of progress
            print_issue(f"Uploading {len(entries)} entries")

            try:
                con = None
                # Creating connection
                con = self.database.cursor()

                # Submitting all entries
                for entry in entries:
                    con.execute(entry)

                # Closing off sesssion
                self.database.commit()
            except Exception as e:
                # Rolling back failed transaction
                if con:
                    con.rollback()

                # Informing of issue
                send_email(f"Failed to commit {len(entries)} due to {e}")

                # Entering all items into a file for later submission
                save_to_file(entries)
            finally:
                # Closing connection if it obtained a connection
                if con:
                    con.close()

            # Informing user of progress
            print_issue(f"Completed {len(entries)} entries")
        else:
            print_issue(f"No entries")
    def commit(self):
        """
        Forces a commits to the database
        """
        # Obtaining items to commit
        items, self.queued_items = self.queued_items, []

        # Comitting items
        thread = Thread(target=self.update_database, args=(items, ))
        thread.start()
    def commit_checker(self):
        """
        Commits every 100 items
        """
        # Checking if a commit is required
        if len(self.queued_items) >= 100:
            self.commit()
    def query_database(self, query):
        """
        Queries the database
        """
        def execute_query(query, con):
            """
            Queries the database
            """
            # Obtaining connection to database
            if con is None:
                con = self.database.cursor()

            # Executing query
            result = con.execute(query)
            result = con.fetchall()

            # Returning an array of one item if it is one column
            if len(result) != 0 and len(result[0]) == 1:
                return [entry[0] for entry in result]
            return result

        try:
            # Trying to answer query
            con = self.database.cursor()
            result = execute_query(query, con)
        except OperationalError as e:
            # Reporting issue which occurred
            send_email(f"Failed to run {query} on database due to {e}")

            # Retrying in two minutes before giving up
            sleep(120)

            # Retrying
            try:
                # Obtaining connection if previously did not get
                result = execute_query(query, con)
            except:
                # Informing user of error
                raise Exception(f"Could not run query")
        except Exception as e:
            # Reporting issue which occurred
            send_email(f"Failed to run {query} on database due to {e}")

            # Informing user of error
            raise Exception(f"Could not run query")
        finally:
            # Closing of session
            if con:
                con.close()

        return result
    def add_game(self, app_id, name, icon):
        """
        Adds a database entry for a game
        """
        # Submitting game
        self.queue_database(f"INSERT INTO public.\"Game\" (app_id, name, icon) VALUES ({app_id}, {name}, {icon})")

        # Adding associated tasks with game
        self.add_task_game(app_id)
        self.commit_checker()
    def add_item(self, market_hash_name, name, app_id, icon, item_name_id):
        """
        Adds a database entry for an item
        """
        # Adding item
        self.queue_database(f"INSERT INTO public.\"Item\" (market_hash_name, name, app_id, icon, item_name_id) VALUES ('{self.clean_market_hash_name(market_hash_name)}', {name}, {app_id}, {icon}, {item_name_id}")

        # Adding associated tasks to item
        self.add_task_item(market_hash_name, app_id)
        self.commit_checker()
    def add_price_daily(self, market_hash_name, time, median_price, volume):
        """
        Adds an item to PriceDaily
        """
        self.queue_database(f"INSERT INTO public.\"PriceDaily\" (market_hash_name, time, median_price, volume) VALUES ('{self.clean_market_hash_name(market_hash_name)}', '{time}'::timestamp, {median_price}, {volume})")
        self.commit_checker()
    def add_price_hourly(self, market_hash_name, time, median_price, volume):
        """
        Adds an item to PriceHourly
        """
        self.queue_database(f"INSERT INTO public.\"PriceHourly\" (market_hash_name, time, median_price, volume) VALUES ('{self.clean_market_hash_name(market_hash_name)}', '{time}'::timestamp, {median_price}, {volume})")
        self.commit_checker()
    def add_price_live(self, market_hash_name, time, sell_price, buy_price, median_price, volume, sell_quantity, buy_quantity, total_sell_quantity, total_buy_quantity):
        """
        Adds an item to PriceLive
        """
        self.queue_database(f"INSERT INTO public.\"PriceLive\" (market_hash_name, time, sell_price, buy_price, median_price, volume, sell_quantity, buy_quantity, total_sell_quantity, total_buy_quantity) VALUES ('{self.clean_market_hash_name(market_hash_name)}', '{time}'::timestamp, {sell_price}, {buy_price}, {median_price}, {volume}, {sell_quantity}, {buy_quantity}, {total_sell_quantity}, {total_buy_quantity})")
        self.commit_checker()
    def add_task_item(self, item, app_id, live_price=True, official_price=True):
        """
        Adds a new item from a game
        """
        if live_price:
            self.queue_database(f"INSERT INTO task (item, app_id, action, due_date, timeout_time) VALUES ('{self.clean_market_hash_name(item)}', {app_id}, 'Live Price', '{datetime.utcnow()}'::timestamp, NULL)")
        if official_price:
            self.queue_database(f"INSERT INTO task (item, app_id, action, due_date, timeout_time) VALUES ('{self.clean_market_hash_name(item)}', {app_id}, 'Official Price', '{datetime.utcnow()}'::timestamp, NULL)")
        self.commit_checker()
    def add_task_game(self, app_id):
        """
        Adds a new game
        """
        self.queue_database(f"INSERT INTO task (item, app_id, action, due_date, timeout_time) VALUES ('Operation Phoenix Weapon Case', {app_id}, 'New Items', '{datetime.utcnow()}'::timestamp, NULL)")
        self.commit_checker()
    def update_task(self, item, app_id, action, failed=False):
        """
        Updates a task
        """
        if failed:
            self.queue_database(f"UPDATE task SET timeout_time=NULL WHERE item='{self.clean_market_hash_name(item)}' AND app_id={app_id} AND action='{action}'")
        else:
            if action == "Live Price":
                # Requires fast updating, preferably on a daily scale
                self.queue_database(f"UPDATE task SET timeout_time=NULL, due_date='{datetime.utcnow() + relativedelta.relativedelta(days=0.5)}'::timestamp WHERE item='{self.clean_market_hash_name(item)}' AND app_id={app_id} AND action='{action}'")
            else:
                # Do not require frequent updates
                self.queue_database(f"UPDATE task SET timeout_time=NULL, due_date='{datetime.utcnow() + relativedelta.relativedelta(days=14)}'::timestamp WHERE item='{self.clean_market_hash_name(item)}' AND app_id={app_id} AND action='{action}'")
        self.commit_checker()
    def obtain_tasks(self):
        """
        Gives tasks out - should not be done like this, does not guarantee no redundancy
        """
        # Obtaining tasks
        tasks = self.query_database("SELECT item, app_id, action FROM task WHERE timeout_time IS NULL OR timeout_time <= timezone('utc', now()) ORDER BY least(timeout_time, due_date) ASC LIMIT 100")

        # Setting tasks as currently being processed
        for task in tasks.copy():
            try:
                if task[2] == "New Items":
                    # Big update to scan for all potential new items
                    self.queue_database(f"UPDATE task SET timeout_time='{datetime.utcnow() + relativedelta.relativedelta(days=3)}'::timestamp WHERE item='{self.clean_market_hash_name(task[0])}' AND app_id={task[1]} AND action='{task[2]}'")
                elif task[2] == "Live Price":
                    # Requires fast processing, one day per point
                    self.queue_database(f"UPDATE task SET timeout_time='{datetime.utcnow() + relativedelta.relativedelta(days=0.25)}'::timestamp WHERE item='{self.clean_market_hash_name(task[0])}' AND app_id={task[1]} AND action='{task[2]}'")
                else:
                    self.queue_database(f"UPDATE task SET timeout_time='{datetime.utcnow() + relativedelta.relativedelta(days=1)}'::timestamp WHERE item='{self.clean_market_hash_name(task[0])}' AND app_id={task[1]} AND action='{task[2]}'")
            except Exception as e:
                # Failed to get item
                log_issue("steam_scraper_stack", f"solve_tasks\tdatabase\ttask={task}\tCouldn't get task {e}")
                tasks.remove(task)
        self.commit()

        # Returning tasks
        return tasks
    def clean_market_hash_name(self, name):
        """
        Used to handle items which have a single quote in their name
        """
        return name.replace("'", "''")
    def get_cookie(self):
        """
        Used to obtain scraping cookie
        """
        return self.query_database("SELECT value FROM information WHERE name='cookie'")[0]
