from steam_database import SteamDatabase

if __name__ == "__main__":
    # Connecting to database
    database = SteamDatabase()

    # Checking if workers have recently pinged
    pings = database.query_database("""
        SELECT distinct name
        FROM workers
        WHERE last_ping >= (timezone('utc', now()) - INTERVAL '0.1 DAY')::timestamp
    """)

    # Printing information of workers
    for ping in pings:
        print(ping)
