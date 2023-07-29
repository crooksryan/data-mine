import os # will be used to determine if external is there
import schedule
# try both options
# os.path.exists()
# os.path.ismount()

import alpaca_trade_api as alpaca
from dotenv.main import load_dotenv
import os
from time import sleep

class StockAPI:
    def __init__(self):
        load_dotenv()
        
        self.key = os.getenv('ALPACAKEY')
        self.secret = os.getenv('ALPACASECRET')
        self.url = 'https://paper-api.alpaca.markets'
        self.api = alpaca.REST(self.key, self.secret, self.url)
    
    def get_bars(self, lst):
        return self.api.get_latest_bars(lst)
    
    def is_open(self):
        return self.api.get_clock().is_open

# TODO: find more stocks for this
stocks = ['aapl', 'voo']
api = StockAPI()


def line(iterations=0):
    if not api.is_open():
        sleep(3600)
        return
    
    try:
        response=api.get_bars(stocks)

        for stock in response.keys():
            with open(f'./data/{stock}.csv', 'a') as file:
                file.write(f'{response[stock].t}, {response[stock].vw}\n')
        
        return None
    except:
        if iterations < 3:
            sleep(30)
            return line(iterations=iterations+1)
        return None

schedule.every().hour.do(line)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        sleep(1800)
