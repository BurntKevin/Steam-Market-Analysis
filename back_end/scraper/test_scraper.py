"""
Tests scraper functions
"""
# Library to test
from scraper import get_item_count, get_items_basic_details_from_page, get_items_basic_details, get_item_price_history_from_page, get_items_price_history
from scraper_data import Item

def test_get_item_count():
    """
    Test item_count
    Tested with a small game as item count will not change too frequently and
    tested with a large game with a range which may return false in the future
    when more items are added
    """
    # Small game - MineSweeper VR
    minesweeper_vr = get_item_count("516940")
    assert minesweeper_vr == 2

    # Large game - Counter-Strike: Global Offensive
    counter_strike_global_offensive = get_item_count("730")
    assert 14000 < counter_strike_global_offensive < 16000

def test_get_items_basic_details_from_page():
    """
    Test get_items_basic_details_from_page
    Tested with a full page of 100 items and a page with under 50 items
    May return false in the future if more items are added to the game with
    less than 50 items (MineSweeper VR)
    """
    # Testing MineSweeper VR with item count and items
    items = get_items_basic_details_from_page("516940", 0)
    assert len(items) == 2
    assert "1$" in items[0].name or "1$" in items[1].name
    assert "5$" in items[0].name or "5$" in items[1].name
    assert "https://steamcommunity.com/economy/image/kwXyVPRfJkeuBOadzgUBV-gOgVokGqIyFmsfT2ir8Ji7CaVx30kHdg" in items[0].icon or "https://steamcommunity.com/economy/image/kwXyVPRfJkeuBOadzgUBV-gOgVokGqIyFmsfT2ir8Ji7CaVx30kHdg" in items[1].icon
    assert "https://steamcommunity.com/economy/image/kwXyVPRfJkeuBOadzgUBV-gOgVokGqIyFmsfT2ir9Ji7CaU56XkIzg" in items[0].icon or "https://steamcommunity.com/economy/image/kwXyVPRfJkeuBOadzgUBV-gOgVokGqIyFmsfT2ir9Ji7CaU56XkIzg" in items[1].icon

    # Testing CS:GO with item count but no items as it varies due to the
    # sorting used by Steam
    items = get_items_basic_details_from_page("730", 0)
    assert len(items) == 100

def test_get_items_basic_details():
    """
    Test get_items_basic_details
    Tested game with less than 50 items (MineSweeperVR), more than 50 items but
    less than 100 items (immune) and more than 100 items (miscreated)
    Tests may fail in the future if items added exceeds the safety net used
    """
    # Getting MineSweeper VR Items
    minesweeper_vr = get_items_basic_details("516940")

    # Creating MineSweeper VR Items which are known to exist
    one_dollar = Item("1$", "kwXyVPRfJkeuBOadzgUBV-gOgVokGqIyFmsfT2ir8Ji7CaVx30kHdg")
    five_dollars = Item("5$", "kwXyVPRfJkeuBOadzgUBV-gOgVokGqIyFmsfT2ir9Ji7CaU56XkIzg")

    # Ensuring that item is obtained
    assert minesweeper_vr.item_exist(one_dollar) is not False
    assert minesweeper_vr.item_exist(five_dollars) is not False

    # Testing under a page of items
    immune = get_items_basic_details("348670")
    assert (50 < immune.item_count() < 100) is True

    # Testing more than a page of items
    miscreated = get_items_basic_details("299740")
    assert (400 < miscreated.item_count() < 500) is True

def test_get_item_price_history_from_page():
    """
    Test get_item_price_history_from_page
    """
    # Obtaining items from MineSweeper VR
    price_history = get_item_price_history_from_page("516940", "1$")

    # Testing to ensure items are obtained
    assert len(price_history) > 30

def test_get_items_price_history():
    """
    Test get_items_price_history
    Tested game with one page of items and game with multiple pages
    """
    # Obtaining items from MineSweeper VR
    minesweeper_vr = get_items_price_history("516940")

    # Creating MineSweeper VR Items which are known to exist
    one_dollar = Item("1$", "kwXyVPRfJkeuBOadzgUBV-gOgVokGqIyFmsfT2ir8Ji7CaVx30kHdg")
    five_dollars = Item("5$", "kwXyVPRfJkeuBOadzgUBV-gOgVokGqIyFmsfT2ir9Ji7CaU56XkIzg")

    # Testing to ensure items are obtained
    assert minesweeper_vr.game_id == "516940"
    assert minesweeper_vr.item_exist(one_dollar) is not False
    assert minesweeper_vr.item_exist(five_dollars) is not False
    assert len(minesweeper_vr.items[0].price_history) > 30 or len(minesweeper_vr.items[1].price_history) > 30
