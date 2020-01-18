"""
Test scraper data
"""
# Supporting functions
from os import remove # To remove file
from datetime import datetime # To format pricehistory date
import sys # To access library

# Library to test
sys.path.insert(0, "../library")
from scraper_data import Game, Item, PriceHistoryPoint
from scraper_support import data_from_pickle_file, get_file_location
from scraper import get_item_price_history_from_page

def test_game_class_init():
    """
    Test game class init
    """
    # Creating object - Counter-Strike: Global Offensive
    counter_strike_global_offensive = Game("730")
    assert counter_strike_global_offensive.game_id == "730" and counter_strike_global_offensive.items == []

def test_game_class_add_item():
    """
    Test game class add_item
    """
    # Creating object - Counter-Strike: Global Offensive
    counter_strike_global_offensive = Game("730")

    # Adding item - Shattered Web Case
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    counter_strike_global_offensive.add_item(shattered_web_case)
    assert counter_strike_global_offensive.items[0] == shattered_web_case

    # Adding a second item - CS20 Case
    cs20_case = Item("CS20 Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFU0naHKIj9D7oTgl4LelaGnMuqIwDgFusR337HCpYmhiwzm8ktqMjv2INKLMlhprbp6CTE")
    counter_strike_global_offensive.add_item(cs20_case)
    assert counter_strike_global_offensive.items[1] == cs20_case

    # Adding a duplicate item - CS20 Case
    counter_strike_global_offensive.add_item(cs20_case)
    assert len(counter_strike_global_offensive.items) == 2 and counter_strike_global_offensive.items[0] == shattered_web_case and counter_strike_global_offensive.items[1] == cs20_case

def test_game_class_item_exist():
    """
    Test game item exist
    """
    # Creating object - Counter-Strike: Global Offensive and Shattered Web Case
    counter_strike_global_offensive = Game("730")
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
    counter_strike_global_offensive = Game("730")
    counter_strike_global_offensive.show()

    # Testing game with skins
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    counter_strike_global_offensive.add_item(shattered_web_case)
    counter_strike_global_offensive.show()

def test_game_class_save():
    """
    Test game save
    """
    # Testing game without skins
    test = Game("test")
    test.save()
    saved_test = data_from_pickle_file(get_file_location("test"))
    assert test.same(saved_test)

    # Testing game with skins
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    test.add_item(shattered_web_case)
    assert test.same(saved_test) is False

    # Cleaning up
    remove(get_file_location("test"))

def test_game_class_item_count():
    """
    Test game item count
    """
    # Testing a game with 0 items
    counter_strike_global_offensive = Game("730")
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
    counter_strike_global_offensive = Game("730")
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    counter_strike_global_offensive.add_item(shattered_web_case)

    # Item the same
    counter_strike_global_offensive_same = Game("730")
    counter_strike_global_offensive_same.add_item(shattered_web_case)
    assert counter_strike_global_offensive.same(counter_strike_global_offensive_same) is True
    assert counter_strike_global_offensive.same(counter_strike_global_offensive)

    # Different game_id
    counter_strike_global_offensive_same = Game("1730")
    counter_strike_global_offensive.add_item(shattered_web_case)
    assert counter_strike_global_offensive.same(counter_strike_global_offensive_same) is False

    # Different items
    counter_strike_global_offensive_same = Game("730")
    assert counter_strike_global_offensive.same(counter_strike_global_offensive_same) is False

def test_item_class_init():
    """
    Test item class init
    """
    # Creating object - Shattered Web Case
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    assert shattered_web_case.name == "Shattered Web Case" and shattered_web_case.icon == "https://steamcommunity.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA" and shattered_web_case.price_history == []

def test_item_add_price_history():
    """
    Test item class add_price_history
    """
    # Creating object - Shattered Web Case
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")

    # Obtaining a price history to insert
    price_history_point = PriceHistoryPoint("Jan 26 2017 01: +0", 2.495, "1")
    shattered_web_case.add_price_history(price_history_point)
    assert shattered_web_case.price_history[0].same(price_history_point)

    # Replacing price history with a new history
    price_history_point = PriceHistoryPoint("Jan 26 2018 01: +0", 2.495, "1")
    shattered_web_case.add_price_history(price_history_point)
    assert shattered_web_case.price_history[0].same(price_history_point)

def test_item_show():
    """
    Test item show
    """
    # Creating item
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    assert shattered_web_case.show() == "Shattered Web Case has icon https://steamcommunity.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA with 0 price history points"

def test_item_same():
    """
    Test item if an item is the same
    Tested same item, different name, different icon, different price history
    """
    # Item to be compared to
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history_point = PriceHistoryPoint("Jan 26 2017 01: +0", 2.495, "1")
    shattered_web_case.add_price_history(price_history_point)

    # Item the same
    shattered_web_case_same = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    shattered_web_case_same.add_price_history(price_history_point)
    assert shattered_web_case.same(shattered_web_case_same) is True
    assert shattered_web_case.same(shattered_web_case) is True

    # Different name
    cs20_case = Item("CS20 Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history_point = PriceHistoryPoint("Jan 26 2017 01: +0", 2.495, "1")
    cs20_case.add_price_history(price_history_point)
    assert shattered_web_case.same(cs20_case) is False

    # Different icon
    shattered_web_case_second = Item("Shattered Web Case", "ab")
    price_history_point = PriceHistoryPoint("Jan 26 2017 01: +0", 2.495, "1")
    shattered_web_case_second.add_price_history(price_history_point)
    assert shattered_web_case.same(shattered_web_case_second) is False

    # Different price history
    shattered_web_case_second = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history_point = PriceHistoryPoint("Jan 26 2018 01: +0", 2.495, "1")
    shattered_web_case_second.add_price_history(price_history_point)
    assert shattered_web_case.same(shattered_web_case_second) is False

def test_pricehistorypoint_class_init():
    """
    Test priceHistoryPoint class init
    """
    # Creating Object - Price History
    price_history_point = ["Jan 26 2017 01: +0", 2.495, "1"]
    price_point = PriceHistoryPoint(price_history_point[0], price_history_point[1], price_history_point[2])
    assert price_point.date == datetime(2017, 1, 26, 0, 0) and price_point.price == 2.495 and price_point.volume == "1"

def test_pricehistorypoint_class_show():
    """
    Test priceHistoryPoint class show
    """
    # Creating price history point
    first_price = PriceHistoryPoint("Nov 18 2019 01: +0", 6.247, "2055")
    assert first_price.show() == "18/11/2019 has price 6.247 and volume 2055"

    # Testing another price history point to ensure that it is dynamic
    second_price = PriceHistoryPoint("Dec 17 2019 13: +0", 1.495, "798")
    assert second_price.show() == "17/12/2019 has price 1.495 and volume 798"

def test_pricehistorypoint_same():
    """
    Test priceHistorypoint same
    Tested same price history point, not same price history point (date, price,
    volume)
    """
    # Testing same price history point
    first_price = PriceHistoryPoint("Nov 18 2019 01: +0", 6.247, "2055")
    second_price = PriceHistoryPoint("Nov 18 2019 01: +0", 6.247, "2055")
    assert first_price.same(first_price)
    assert first_price.same(second_price)

    # Testing different date
    third_price = PriceHistoryPoint("Nov 18 2020 01: +0", 6.247, "2055")
    assert first_price.same(third_price) is False

    # Testing different price
    third_price = PriceHistoryPoint("Nov 18 2019 01: +0", 2, "2055")
    assert first_price.same(third_price) is False

    # Testing different volume
    third_price = PriceHistoryPoint("Nov 18 2019 01: +0", 6.247, "20552")
    assert first_price.same(third_price) is False
