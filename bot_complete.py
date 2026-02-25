import yfinance as yf
from datetime import datetime

class StockAnalyzer:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self.data = None

    def fetch_data(self):
        self.data = yf.download(self.stock_symbol, period='1d', interval='1m')
        return self.data

    def analyze(self):
        # Perform technical analysis. Placeholder for simplicity.
        if self.data is not None:
            close_prices = self.data['Close']
            return close_prices[-1] # Return the latest close price

class Bot:
    def __init__(self):
        self.stock_analyzer = None

    def set_stock(self, stock_symbol):
        self.stock_analyzer = StockAnalyzer(stock_symbol)

    def get_stock_analysis(self):
        if self.stock_analyzer:
            data = self.stock_analyzer.fetch_data()
            latest_price = self.stock_analyzer.analyze()
            return {'data': data, 'latest_price': latest_price}
        return None

# Example of using the bot:
if __name__ == '__main__':
    bot = Bot()
    stock_symbol = 'AAPL'  # Example stock
    bot.set_stock(stock_symbol)
    analysis_result = bot.get_stock_analysis()
    print(f"Analysis Result for {stock_symbol}: {analysis_result}")
    
# Proper button handlers would be implemented with a GUI framework or web framework.
