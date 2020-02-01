"""
Test scraper data
"""
# Supporting functions
from datetime import datetime # To format pricehistory date

# Library to test
from back_end.scraper.application.scraper_data import Game, Item, PriceHistoryPoint

def test_game_class_init():
    """
    Test game class init
    """
    # Creating object - Counter-Strike: Global Offensive
    counter_strike_global_offensive = Game(730)
    assert counter_strike_global_offensive.name == "Counter-Strike: Global Offensive"
    assert counter_strike_global_offensive.game_id == 730
    assert counter_strike_global_offensive.items == []

def test_game_class_add_item():
    """
    Test game class add_item
    """
    # Creating object - Counter-Strike: Global Offensive
    counter_strike_global_offensive = Game(730)

    # Adding item - Shattered Web Case
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    counter_strike_global_offensive.add_item(shattered_web_case)
    assert counter_strike_global_offensive.item_exist(shattered_web_case)

    # Adding a second item - CS20 Case
    cs20_case = Item("CS20 Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU0naHKIj9D7oTgl4LelaGnMuqIwDgFusR337HCpYmhiwzm8ktqMjv2INKLMlhprbp6CTE")
    counter_strike_global_offensive.add_item(cs20_case)
    assert counter_strike_global_offensive.item_exist(cs20_case)

    # Adding a duplicate item - CS20 Case
    counter_strike_global_offensive.add_item(cs20_case)
    assert len(counter_strike_global_offensive.items) == 2
    assert counter_strike_global_offensive.item_exist(shattered_web_case)
    assert counter_strike_global_offensive.item_exist(cs20_case)

def test_game_class_item_exist():
    """
    Test game item exist
    """
    # Creating object - Counter-Strike: Global Offensive and Shattered Web Case
    counter_strike_global_offensive = Game(730)
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")

    # Item does not currently exist - Shattered Web Case
    assert counter_strike_global_offensive.item_exist(shattered_web_case) is False

    # Adding item, item exists - Shattered Web Case
    counter_strike_global_offensive.add_item(shattered_web_case)
    assert counter_strike_global_offensive.item_exist(shattered_web_case) is not False

def test_game_class_show():
    """
    Test game show
    """
    # Testing game without skins
    counter_strike_global_offensive = Game(730)
    counter_strike_global_offensive.show()

    # Testing game with skins
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    counter_strike_global_offensive.add_item(shattered_web_case)
    counter_strike_global_offensive.show()

def test_game_class_item_count():
    """
    Test game item count
    """
    # Testing a game with 0 items
    counter_strike_global_offensive = Game(730)
    assert counter_strike_global_offensive.item_count() == 0

    # Testing a game with 1 item
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    counter_strike_global_offensive.add_item(shattered_web_case)
    assert counter_strike_global_offensive.item_count() == 1

    # Testing a game with 110 items
    for i in range(109):
        new_item = Item(i, i)
        counter_strike_global_offensive.add_item(new_item)
    assert counter_strike_global_offensive.item_count() == 110

def test_game_same():
    """
    Test game same
    Testing same game, different game_id, different items
    """
    # Item to be compared to
    counter_strike_global_offensive = Game(730)
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    counter_strike_global_offensive.add_item(shattered_web_case)

    # Item the same
    counter_strike_global_offensive_same = Game(730)
    counter_strike_global_offensive_same.add_item(shattered_web_case)
    assert counter_strike_global_offensive.same(counter_strike_global_offensive_same)
    assert counter_strike_global_offensive.same(counter_strike_global_offensive)

    # Different game_id
    counter_strike_global_offensive_same = Game(1730)
    counter_strike_global_offensive.add_item(shattered_web_case)
    assert counter_strike_global_offensive.same(counter_strike_global_offensive_same) is False

    # Different items
    counter_strike_global_offensive_same = Game(730)
    assert counter_strike_global_offensive.same(counter_strike_global_offensive_same) is False

def test_game_deobject():
    """
    Test deobject game
    """
    # Testing no item game
    counter_strike_global_offensive = Game(730)
    assert counter_strike_global_offensive.deobject() == {
        "game_id": 730,
        "items": []
    }

def test_game_game_icon():
    """
    Test game icon
    """
    # Testing CS:GO
    counter_strike_global_offensive = Game(730)
    assert counter_strike_global_offensive.game_icon() == "https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg"

    # Testing Minesweeper VR
    minesweeper_vr = Game(516940)
    assert minesweeper_vr.game_icon() == "https://steamcdn-a.akamaihd.net/steam/apps/516940/header.jpg"

def test_item_class_init():
    """
    Test item class init
    """
    # Creating object - Shattered Web Case
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    assert shattered_web_case.name == "Shattered Web Case"
    assert shattered_web_case.icon == "https://steamcommunity.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA"
    assert shattered_web_case.price_history == []

def test_item_add_price_history():
    """
    Test item class add_price_history
    """
    # Creating object - Shattered Web Case
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")

    # Obtaining a price history to insert
    price_history_point_1 = PriceHistoryPoint(datetime(2017, 1, 26), 2.495, 1)
    shattered_web_case.add_price_history([price_history_point_1])
    assert shattered_web_case.price_history[0].same(price_history_point_1)

    # Replacing price history with a new history
    price_history_point_2 = PriceHistoryPoint(datetime(2017, 1, 22), 2.495, 1)
    shattered_web_case.add_price_history([price_history_point_2])
    assert shattered_web_case.price_history[0].same(price_history_point_2)
    assert shattered_web_case.price_history[0].same(price_history_point_1) is False

def test_item_show():
    """
    Test item show
    Tested item with no price history, item with price history
    """
    # Item with no price history
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    assert shattered_web_case.show() == "Shattered Web Case has icon https://steamcommunity.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA with 0 price history points"

    # Item with price history
    price_history_point = PriceHistoryPoint(datetime(2017, 1, 26), 2.495, 1)
    shattered_web_case.add_price_history([price_history_point])
    assert shattered_web_case.show() == "Shattered Web Case has icon https://steamcommunity.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA with 1 price history points"

def test_item_same():
    """
    Test item if an item is the same
    Tested same item, different name, different icon, different price history
    """
    # Item to be compared to
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history_point = [PriceHistoryPoint(datetime(2017, 1, 26), 2.495, 1)]
    shattered_web_case.add_price_history(price_history_point)

    # Item the same
    shattered_web_case_same = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    shattered_web_case_same.add_price_history(price_history_point)
    assert shattered_web_case.same(shattered_web_case_same) is True
    assert shattered_web_case.same(shattered_web_case) is True

    # Different name
    cs20_case = Item("CS20 Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history_point = [PriceHistoryPoint(datetime(2017, 1, 26), 2.495, 1)]
    cs20_case.add_price_history(price_history_point)
    assert shattered_web_case.same(cs20_case) is False

    # Different icon
    shattered_web_case_second = Item("Shattered Web Case", "ab")
    price_history_point = [PriceHistoryPoint(datetime(2017, 1, 26), 2.495, 1)]
    shattered_web_case_second.add_price_history(price_history_point)
    assert shattered_web_case.same(shattered_web_case_second) is False

    # Different price history
    shattered_web_case_second = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history_point = [PriceHistoryPoint(datetime(2017, 1, 22), 2.495, 1)]
    shattered_web_case_second.add_price_history(price_history_point)
    assert shattered_web_case.same(shattered_web_case_second) is False

def test_item_deobject():
    """
    Test item deobject
    """
    shattered_web_case = Item("Shattered Web Case", "link")
    assert shattered_web_case.deobject() == {
        "item_name": "Shattered Web Case",
        "item_icon": "https://steamcommunity.com/economy/image/link",
        "price_history": []
    }

def test_pricehistorypoint_class_init():
    """
    Test priceHistoryPoint class init
    """
    # Creating Object - Price History
    price_point = PriceHistoryPoint(datetime(2017, 1, 26, 0, 0), 2.495, 1)
    assert price_point.date == datetime(2017, 1, 26, 0, 0)
    assert price_point.price == 2.495
    assert price_point.volume == 1
    assert price_point.rsi is None
    assert price_point.macd is None
    assert price_point.percentage_change is None
    assert price_point.turnover == 2.495

def test_pricehistorypoint_class_show():
    """
    Test priceHistoryPoint class show
    """
    # Creating price history point
    first_price = PriceHistoryPoint(datetime(2019, 11, 18, 0, 0), 6.247, 2055)
    assert first_price.show() == "18/11/2019 has price 6.247 and volume 2055"

    # Testing another price history point to ensure that it is dynamic
    second_price = PriceHistoryPoint(datetime(2019, 12, 17, 0, 0), 1.495, 798)
    assert second_price.show() == "17/12/2019 has price 1.495 and volume 798"

def test_pricehistorypoint_same():
    """
    Test priceHistorypoint same
    Tested same price history point, not same price history point (date, price,
    volume)
    """
    # Testing same price history point
    first_price = PriceHistoryPoint(datetime(2017, 1, 26), 6.247, 2055)
    second_price = PriceHistoryPoint(datetime(2017, 1, 26), 6.247, 2055)
    assert first_price.same(first_price)
    assert first_price.same(second_price)

    # Testing different date
    third_price = PriceHistoryPoint(datetime(2017, 1, 12), 6.247, 2055)
    assert first_price.same(third_price) is False

    # Testing different price
    third_price = PriceHistoryPoint(datetime(2017, 1, 26), 2, 2055)
    assert first_price.same(third_price) is False

    # Testing different volume
    third_price = PriceHistoryPoint(datetime(2017, 1, 26), 6.247, 20552)
    assert first_price.same(third_price) is False

def test_pricehistorypoint_deobject():
    """
    Test price history point deobject
    """
    price = PriceHistoryPoint(datetime(2017, 1, 26), 6.247, 20552)
    assert price.deobject() == {
        "price_history_point_date": datetime(2017, 1, 26),
        "price_history_point_price": 6.247,
        "price_history_point_volume": 20552,
        "price_history_point_rsi": None,
        "price_history_point_macd": None,
        "price_history_point_percentage_change": None,
        "price_history_point_turnover": 128388.344
    }
