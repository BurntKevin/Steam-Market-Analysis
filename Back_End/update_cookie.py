"""
Changes the cookie of the database
"""
import sys
from steam_database import SteamDatabase

if __name__ == "__main__":
    # Creating database
    database = SteamDatabase()

    # Obtaining all items which have a timeout
    work = database.update_database([
        f"""
        UPDATE information
        SET value='{sys.argv[1]}'
        where name='cookie'
        """
    ])

    # Closing session
    database.shutdown()
