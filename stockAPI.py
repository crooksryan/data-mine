import alpaca_trade_api as alpaca
from dotenv.main import load_dotenv
import os


class StockAPI:
    def __init__(self):
        load_dotenv()

        self.key = os.getenv('ALPACAKEY')
        self.secret = os.getenv('ALPACASECRET')
        self.url = 'https://paper-api.alpaca.markets'
        self.api = alpaca.REST(self.key, self.secret, self.url)
        self.stocks = ['aapl', 'amzn', 'voo', 'goog']

    def get_bars(self, lst):
        return self.api.get_latest_bars(lst)

    def get_historical(self, lst, date):
        return self.api.get_bars(lst, '2hour',
                                 start=date,
                                 limit=5,
                                 adjustment='all')

    def is_open(self):
        return self.api.get_clock().is_open


if __name__ == '__main__':
    print(StockAPI().get_historical('aapl', '2023-08-01')[0])
