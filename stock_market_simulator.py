from datetime import datetime, timedelta
from math import prod


class Stock:
    def __init__(self, symbol, stock_type, last_dividend, fixed_dividend, par_value):
        """
        Initialize a Stock object.

        :param symbol: Stock symbol.
        :param stock_type: Type of stock (either 'Common' or 'Preferred').
        :param last_dividend: The last dividend paid by the stock.
        :param fixed_dividend: The fixed dividend percentage (only applicable for 'Preferred' stocks).
        :param par_value: The par value of the stock.
        """
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = []

    def dividend_yield(self, price):
        """
        Calculate the Dividend Yield for the stock.

        :param price: Current price of the stock.
        :return: Dividend Yield value.
        """
        if self.stock_type == 'Common':
            return self.last_dividend / price
        elif self.stock_type == 'Preferred':
            return (self.fixed_dividend * self.par_value) / price

    def pe_ratio(self, price):
        """
        Calculate the P/E Ratio for the stock.

        :param price: Current price of the stock.
        :return: P/E Ratio value.
        """
        return price / self.last_dividend

    def record_trade(self, quantity, action, price):
        """
        Record a trade for the stock.

        :param quantity: Number of shares traded.
        :param action: Type of trade action ('buy' or 'sell').
        :param price: Price at which the trade occurred.
        """
        self.trades.append({
            'timestamp': datetime.now(),
            'quantity': quantity,
            'action': action,
            'price': price,
        })

    def volume_weighted_stock_price(self):
        """
        Calculate the Volume Weighted Stock Price (VWAP) for the stock.

        :return: Volume Weighted Stock Price value.
        """
        now = datetime.now()
        past_15_minutes_trades = [trade for trade in self.trades if now - trade['timestamp'] <= timedelta(minutes=15)]
        trade_sum = sum([trade['quantity'] * trade['price'] for trade in past_15_minutes_trades])
        quantity_sum = sum([trade['quantity'] for trade in past_15_minutes_trades])
        return trade_sum / quantity_sum


class StockMarket:
    def __init__(self, stocks):
        """
        Initialize a StockMarket object.

        :param stocks: List of Stock objects.
        """
        self.stocks = {stock.symbol: stock for stock in stocks}

    def gbce_all_share_index(self):
        """
        Calculate the GBCE All Share Index for all stocks in the market.

        :return: GBCE All Share Index value.
        """
        prices = []
        for stock in self.stocks.values():
            prices.extend([trade['price'] for trade in stock.trades])
        return (prod(prices)) ** (1.0 / len(prices))


# Example usage of the classes and methods
tea = Stock('TEA', 'Common', 0, None, 100)
pop = Stock('POP', 'Common', 8, None, 100)
ale = Stock('ALE', 'Common', 23, None, 60)
gin = Stock('GIN', 'Preferred', 8, 0.02, 100)
joe = Stock('JOE', 'Common', 13, None, 250)

gbce = StockMarket([tea, pop, ale, gin, joe])

tea.record_trade(100, 'buy', 110)
pop.record_trade(200, 'sell', 120)
ale.record_trade(150, 'buy', 130)
gin.record_trade(250, 'sell', 140)
joe.record_trade(300, 'buy', 150)

print('Dividend Yield for TEA:', tea.dividend_yield(110))
print('P/E Ratio for POP:', pop.pe_ratio(120))
print('Volume Weighted Stock Price for ALE:', ale.volume_weighted_stock_price())
print('GBCE All Share Index:', gbce.gbce_all_share_index())
