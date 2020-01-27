import datetime

def prices_from_start_date_to_end_date(price_history):
    prices = []
    for price_history_point in price_history:
        prices.append(price_history_point.price)

    return prices