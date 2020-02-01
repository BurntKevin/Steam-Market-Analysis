import datetime

def prices_from_start_date_to_end_date(price_history):
    prices = []
    for price_history_point in price_history:
        prices.append(price_history_point.price)

    return prices

def get_prices_from_price_history(prices):
    prices = []
    for point in price_history:
        prices.append(point.price)

    return prices

def average_loss(prices):
    """
    Calculates the average loss
    """
    # Loss variables
    loss_days = 0
    sum_loss_percentage = 0

    # Obtaining average loss
    previous_price = None
    for price in prices:
        # Not first price, able to calculate loss
        if previous_price is not None:
            if price < previous_price:
                # Price has decreased
                loss_days += 1
                sum_loss_percentage += price / previous_price

        previous_price = price

    return sum_loss_percentage / loss_days

def average_gain(prices):
    """
    Calculates the average gain
    """
    # Gain variables
    gain_days = 0
    sum_gain_percentage = 0

    # Obtaining average gain
    previous_price = None
    for price in prices:
        # Not first price, able to calculate
        if previous_price is not None:
            if price > previous_price:
                # Price has increased
                gain_days += 1
                sum_gain_percentage += 1 - price / previous_price
        
        previous_price = price

    return sum_gain_percentage / gain_days

def calculate_rsi(prices):
    """
    Calculates the rsi for a given length of prices
    RSI formula: 100 - (100 / (1 + average_gain / average_loss))
    """
    return 100 - (100 / (1 + average_gain(prices) / average_loss(prices)))
