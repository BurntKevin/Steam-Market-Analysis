from back_end.technical_analysis.support import get_prices_from_price_history, calculate_rsi

"""
Incomplete, completing core functionality first
"""
def calculate_rsi_from_price_history(price_history):
    """
    Using standard RSI formula of 14 days
    RSI formula: 100 - (100 / (1 + average_gain_of_14_days / average_loss_of_14_days))
    """
    # Getting a list of the corresponding prices
    prices = get_prices_from_price_history(price_history)

    # Filling data points which cannot generate an rsi
    for price_history 

    # Appending corresponding rsi for each respective data point
    for i in range(13, len(prices) - 13):
        # Obtaining average gain
        rsi = calculate_rsi(prices[i:i + 14])
        
        ret

    day = 0
    for price_history_point in price_history:
        if day < 14:
            # Insufficient data to make RSI calculation
            day += 1
        else:
            pass




price_history_point["price_history_point_rsi"]