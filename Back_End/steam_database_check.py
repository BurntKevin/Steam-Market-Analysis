"""
Checks the validity of data in the database and also fixes issues with data integrity
"""
# Personal
from steam_database import SteamDatabase

def check_for_tasks():
    """
    Checks if all items have their corresponding tasks, if not, create them
    """
    # Creating database
    database = SteamDatabase()

    tasks = set(database.query_database("SELECT item, app_id, action FROM task"))
    items = database.query_database('SELECT market_hash_name, app_id FROM public."Item"')
    games = database.query_database('SELECT app_id FROM public."Game"')

    # Checking games
    for game in games:
        # Operation Phoenix Weapon Case is a placeholder to pass foreign key - mostly because I don't want another table of items or to split it
        if ("Operation Phoenix Weapon Case", game, "New Items") not in tasks:
            # Add actions associated with game
            database.add_task_game(game)

    # Checking items
    for item in items:
        if (item[0], item[1], "Official Price") not in tasks:
            # Add actions associated with item
            database.add_task_item(item[0], item[1], live_price=False)
        if (item[0], item[1], "Live Price") not in tasks:
            # Add actions associated with item
            database.add_task_item(item[0], item[1], official_price=False)

    # Finalising database
    database.shutdown()

if __name__ == "__main__":
    # Running validation of data checks
    check_for_tasks()
