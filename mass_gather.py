# this file will be for getting stock price at EOD for the last 7 years

from datetime import datetime, timedelta
from time import sleep, time
from stockAPI import StockAPI


def get_dates_last_x_years(x):
    start_date = datetime.now() - timedelta(days=365*x)
    end_date = datetime.now()
    delta = timedelta(days=1)

    dates_list = []
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        dates_list.append(date_str)
        current_date += delta

    return dates_list


def is_weekend(date):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please provide the date in the format 'YYYY-MM-DD'.")
        return False

    return date_obj.weekday() in (5, 6)


api = StockAPI()
dates = get_dates_last_x_years(7)

numberOfCalls = 0

# security measure
attempt = input("Enter 'confirm' to run: ")

if attempt != 'confirm':
    exit()

start = time()
for stock in api.stocks:
    with open(f'./data/{stock}.csv', 'w') as file:
        file.write('date,price\n')

    print(f'getting data for {stock}')
    print(f"getting price for {len(dates)} dates")
    print(f'first date: {dates[0]}')
    with open(f'./data/{stock}.csv', 'a') as file:
        for date in dates:
            if is_weekend(date):
                continue

            numberOfCalls += 5
            if numberOfCalls >= 190:
                numberOfCalls = 0
                print(f'Sleeping for 61 seconds for date: {date}')
                sleep(61)

            try:
                bars = api.get_historical(stock, date)
                for bar in bars:
                    price = bar.vw
                    date = str(bar.t).replace('-04:00', '')
                    file.write(f'{date},{price}\n')
            except Exception as e:
                print(f'failed to get price at: {date}\nDue to: {e}')
                sleep(30)

print(f'Ran in {time()-start} seconds')
