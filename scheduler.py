from stockAPI import StockAPI
import schedule
from time import sleep

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

import requests

api = StockAPI()

def getData(iterations=0):
    # will get the stock price for every stock if market is open
    try:
        if not api.is_open():
            return
        
        for stock in api.stocks:
            bar = api.get_bars(stock)
            price = bar.vw
            date = str(bar.t).replace('4:00', '')
            
            with open(f'./data/{stock}.cs', 'a') as file:
                file.write(f'{date},{price}\n')
    except:
        if iterations < 10:
            sleep(60)
            return getData(iterations=iterations+1)



def machine():
    # will produce ML algo
    import warnings
    warnings.filterwarnings('ignore')

    try:
        for stock in api.stocks:
            print(f'Training for {stock}')
            data = pd.read_csv(f'./data/{stock}.csv')

            data['date'] = pd.to_datetime(data['date'])

            price_data = data.filter(['price'])
            dataset = price_data.values
            training = int(np.ceil(len(dataset)))

            scaler = MinMaxScaler(feature_range=(0,1))
            scaled_data = scaler.fit_transform(dataset)


            train_data = scaled_data[0:int(training), :]

            x_train = []
            y_train = []

            for i in range(60, len(train_data)):
                x_train.append(train_data[i-60:i, 0])
                y_train.append(train_data[i, 0])

            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            model = keras.models.Sequential()
            model.add(keras.layers.LSTM(units=64,
                                        return_sequences=True,
                                        input_shape=(x_train.shape[1], 1)))
            model.add(keras.layers.LSTM(units=64))
            model.add(keras.layers.Dense(32))
            model.add(keras.layers.Dropout(0.5))
            model.add(keras.layers.Dense(1))

            model.compile(optimizer=keras.optimizers.Nadam(),
                        loss='mean_squared_error')
            model.fit(x_train, y_train, epochs=80)

            print(f'Saving: {stock} model')
            model.save(f'./models/{stock}.keras')
    except Exception as e:
        print(e)
    return

def predictions():
    # will make predictions when right before market open
    # this will also handle reporting
        # might report to the flask server
        # might also send out email
    try:
        for stock in api.stocks:
            model = keras.models.load_model(f'./models/{stock}.keras')


    except Exception as e:
        print(e)

# scheduling getData for every 2 hours
# schedule.every().day.at('8:00').do(getData)
# schedule.every().day.at('10:00').do(getData)
# schedule.every().day.at('12:00').do(getData)
# schedule.every().day.at('14:00').do(getData)
# schedule.every().day.at('16:00').do(getData)


# # schedule machine for midnight
# schedule.every().day.at('0:00').do(machine)


# # schedule predictions for 7
# schedule.every().day.at('7:00').do(predictions)


# while True:
#     schedule.run_pending()
#     sleep(1)

# machine()
