from back_end.technical_analysis.support import prices_from_start_date_to_end_date

"""
Incomplete, completing core functionality first
"""
def calculate_rsi_from_price_history(price_history):
    """
    Using standard RSI formula of 14 days
    RSI formula: 100 - (100 / (1 + average_gain/average_loss))
    """
    pass

    prices = get_prices(price_history)

    day = 0
    for price_history_point in price_history:
        if day < 14:
            # Insufficient data to make RSI calculation
            day += 1
        else:
            pass