"""
Resets the timeout for items which may be stuck in limbo for an unnecessarily
long time
"""

from steam_database import SteamDatabase

if __name__ == "__main__":
    # Creating database
    database = SteamDatabase()

    # Obtaining all items which have a timeout
    work = database.query_database("""
        SELECT item, app_id, action
        FROM task
        WHERE timeout_time IS NOT NULL
    """)

    # Removing timeouts
    for item in work:
        database.update_task(item[0], item[1], item[2], True)

    # Closing session
    database.shutdown()
