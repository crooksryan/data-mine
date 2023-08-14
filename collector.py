import schedule
# try both options
# os.path.exists()
# os.path.ismount()

import os
from time import sleep
from stockAPI import StockAPI

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
            with open(f'D/{stock}.csv', 'a') as file:
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
