"""
Test scraper data
"""
# Supporting functions
from datetime import datetime # To format pricehistory date

# Library to test
from scraper_data import Game, Item, PriceHistoryPoint

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
    price_history_point_1 = PriceHistoryPoint(datetime(2017, 1, 26), 3, 1)
    shattered_web_case.add_price_history([price_history_point_1])
    assert shattered_web_case.price_history[0].same(price_history_point_1)

    # Replacing price history with a new history
    price_history_point_2 = PriceHistoryPoint(datetime(2017, 1, 22), 3, 1)
    shattered_web_case.add_price_history([price_history_point_2])
    assert shattered_web_case.price_history[0].same(price_history_point_2)
    assert shattered_web_case.price_history[0].same(price_history_point_1) is False

    # Adding price history which fills
    shattered_web_case.add_price_history([price_history_point_2, price_history_point_1])
    assert len(shattered_web_case.price_history) == 5

    # # Testing add_percentage_change functionality
    # price_history_point_3 = PriceHistoryPoint(datetime(2017, 1, 23), 1.5, 1)
    # shattered_web_case.add_price_history([price_history_point_2, price_history_point_3])
    # assert shattered_web_case.price_history[1].percentage_change == 0.5

def test_item_fill_price_history():
    """
    Test item fill price history
    """
    # Testing dates
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history_point_1 = PriceHistoryPoint(datetime(2017, 1, 26), 3, 1)
    price_history_point_2 = PriceHistoryPoint(datetime(2017, 1, 22), 3, 1)
    shattered_web_case.add_price_history([price_history_point_2, price_history_point_1])
    assert len(shattered_web_case.price_history) == 5

def test_item_add_percentage_change():
    """
    Test item add percentage change
    """
    # Creating item
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history_point = PriceHistoryPoint(datetime(2017, 1, 22), 3, 1)

    # Testing stagnant price
    price_history_addition = PriceHistoryPoint(datetime(2017, 1, 23), 3, 1)
    shattered_web_case.add_price_history([price_history_point, price_history_addition])
    assert shattered_web_case.price_history[1].percentage_change == 0

    # Testing increase price
    price_history_addition = PriceHistoryPoint(datetime(2017, 1, 23), 6, 1)
    shattered_web_case.add_price_history([price_history_point, price_history_addition])
    assert shattered_web_case.price_history[1].percentage_change == 1

    # Testing decrease price
    price_history_addition = PriceHistoryPoint(datetime(2017, 1, 23), 1.5, 1)
    shattered_web_case.add_price_history([price_history_point, price_history_addition])
    assert shattered_web_case.price_history[1].percentage_change == 0.5

    # Testing no price
    price_history_addition = PriceHistoryPoint(datetime(2017, 1, 23), None, 0)
    shattered_web_case.add_price_history([price_history_point, price_history_addition])
    assert shattered_web_case.price_history[1].percentage_change is None

def test_item_add_rsi_analaysis():
    """
    Test item add rsi analysis
    """
    # Creating item details
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history = [
        PriceHistoryPoint(datetime(2017, 1, 1), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 2), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 3), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 4), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 5), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 6), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 7), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 8), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 9), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 10), 8, 1),
        PriceHistoryPoint(datetime(2017, 1, 11), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 12), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 13), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 14), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 15), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 16), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 17), 7, 1)
    ]
    shattered_web_case.add_price_history(price_history)

    assert shattered_web_case.price_history[13].rsi is None
    assert shattered_web_case.price_history[14].rsi == 52.94117647058823
    assert shattered_web_case.price_history[15].rsi == 56.75675675675676

def test_item_calculate_rsi_for_point():
    """
    Test item calculate rsi for point
    """
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history = [
        PriceHistoryPoint(datetime(2017, 1, 1), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 2), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 3), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 4), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 5), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 6), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 7), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 8), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 9), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 10), 8, 1),
        PriceHistoryPoint(datetime(2017, 1, 11), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 12), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 13), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 14), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 15), 10, 1)
    ]
    shattered_web_case.price_history = price_history

    shattered_web_case.calculate_rsi_for_point(14)
    assert shattered_web_case.price_history[14].rsi == 60.00000000000001

def test_item_add_macd_analysis():
    """
    Test item add macd analysis
    """
    # Creating item history
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history = [
        PriceHistoryPoint(datetime(2017, 1, 1), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 2), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 3), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 4), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 5), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 6), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 7), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 8), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 9), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 10), 8, 1),
        PriceHistoryPoint(datetime(2017, 1, 11), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 12), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 13), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 14), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 15), 6, 1),
        PriceHistoryPoint(datetime(2017, 1, 16), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 17), 14, 1),
        PriceHistoryPoint(datetime(2017, 1, 18), 13, 1),
        PriceHistoryPoint(datetime(2017, 1, 19), 12, 1),
        PriceHistoryPoint(datetime(2017, 1, 20), 15, 1),
        PriceHistoryPoint(datetime(2017, 1, 21), 13, 1),
        PriceHistoryPoint(datetime(2017, 1, 22), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 23), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 24), 8, 1),
        PriceHistoryPoint(datetime(2017, 1, 25), 12, 1),
        PriceHistoryPoint(datetime(2017, 1, 26), 14, 1),
        PriceHistoryPoint(datetime(2017, 1, 27), 18, 1),
        PriceHistoryPoint(datetime(2017, 1, 28), 15, 1)
    ]
    shattered_web_case.price_history = price_history

    # Testing
    shattered_web_case.add_macd_analysis()
    assert shattered_web_case.price_history[25].macd is None
    assert shattered_web_case.price_history[26].macd == 9.958315673671807
    assert shattered_web_case.price_history[27].macd == 9.516485532043287

def test_item_calculate_macd_of_point():
    """
    Test item calculate macd of point
    """
    # Creating item history
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history = [
        PriceHistoryPoint(datetime(2017, 1, 1), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 2), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 3), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 4), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 5), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 6), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 7), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 8), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 9), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 10), 8, 1),
        PriceHistoryPoint(datetime(2017, 1, 11), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 12), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 13), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 14), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 15), 6, 1),
        PriceHistoryPoint(datetime(2017, 1, 16), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 17), 14, 1),
        PriceHistoryPoint(datetime(2017, 1, 18), 13, 1),
        PriceHistoryPoint(datetime(2017, 1, 19), 12, 1),
        PriceHistoryPoint(datetime(2017, 1, 20), 15, 1),
        PriceHistoryPoint(datetime(2017, 1, 21), 13, 1),
        PriceHistoryPoint(datetime(2017, 1, 22), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 23), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 24), 8, 1),
        PriceHistoryPoint(datetime(2017, 1, 25), 12, 1),
        PriceHistoryPoint(datetime(2017, 1, 26), 14, 1),
        PriceHistoryPoint(datetime(2017, 1, 27), 18, 1),
        PriceHistoryPoint(datetime(2017, 1, 28), 15, 1)
    ]
    shattered_web_case.price_history = price_history

    shattered_web_case.calculate_macd_of_point(25)
    assert shattered_web_case.price_history[25].macd is None
    shattered_web_case.calculate_macd_of_point(26)
    assert shattered_web_case.price_history[26].macd == 9.958315673671807
    shattered_web_case.calculate_macd_of_point(27)
    assert shattered_web_case.price_history[27].macd == 9.516485532043287

def test_item_calculate_ema():
    """
    Test item calculate ema
    """
    # Creating item history
    shattered_web_case = Item("Shattered Web Case", "-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFUznaCaJWVDvozlzdONwvKjYLiBk24IsZEl0uuYrNjw0A3n80JpZWzwIYWLMlhpLvhcskA")
    price_history = [
        PriceHistoryPoint(datetime(2017, 1, 1), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 2), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 3), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 4), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 5), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 6), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 7), 3, 1),
        PriceHistoryPoint(datetime(2017, 1, 8), 4, 1),
        PriceHistoryPoint(datetime(2017, 1, 9), 2, 1),
        PriceHistoryPoint(datetime(2017, 1, 10), 8, 1),
        PriceHistoryPoint(datetime(2017, 1, 11), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 12), 9, 1),
        PriceHistoryPoint(datetime(2017, 1, 13), 7, 1),
        PriceHistoryPoint(datetime(2017, 1, 14), 5, 1),
        PriceHistoryPoint(datetime(2017, 1, 15), 10, 1)
    ]
    shattered_web_case.price_history = price_history

    # Testing unsuccessful
    assert shattered_web_case.calculate_ema(1, 20) is None

    # Testing successful - 1 ema
    assert shattered_web_case.calculate_ema(0, 1) is None
    assert shattered_web_case.calculate_ema(1, 1) == 4
    assert shattered_web_case.calculate_ema(2, 1) == 3
    assert shattered_web_case.calculate_ema(3, 1) == 5

    # Testing successful - 3 ema
    assert shattered_web_case.calculate_ema(2, 3) is None
    assert shattered_web_case.calculate_ema(3, 3) == 2.5
    assert shattered_web_case.calculate_ema(4, 3) == 2.25
    assert shattered_web_case.calculate_ema(4, 3, 2.5) == 2.25

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
