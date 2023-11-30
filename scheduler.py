from stockAPI import StockAPI
import schedule
from time import sleep

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from datetime import datetime, timedelta
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
    except Exception:
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

            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(dataset)

            train_data = scaled_data[0:int(training), :]

            x_train = []
            y_train = []

            for i in range(60, len(train_data)):
                x_train.append(train_data[i-60:i, 0])
                y_train.append(train_data[i, 0])

            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train,
                                 (x_train.shape[0], x_train.shape[1], 1))

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


# TODO: make the predictions and model system better
    # honestly, no idea what this does but it isn't good
def predictions():
    if not api.is_open:
        return

    try:
        totalPre = {}
        for stock in api.stocks:
            model = keras.models.load_model(f'./models/{stock}.keras')
            scaler = MinMaxScaler(feature_range=(0, 1))

            data = pd.read_csv(f'./data/{stock}.csv')

            price_data = data.filter(['price'])
            dataset = price_data.values
            scaled_data = scaler.fit_transform(dataset)

            future_input_data = []

            start_index = len(scaled_data) - 60
            end_index = start_index + 60

            future_input_sequence = scaled_data[start_index:end_index, 0]
            future_input_data.append(future_input_sequence)

            future_input_data = np.array(future_input_data)

            future_input_data = np.reshape(
                    future_input_data,
                    (future_input_data.shape[0],
                     future_input_data.shape[1],
                     1))

            future_predictions = model.predict(future_input_data)

            future_predictions = scaler.inverse_transform(future_predictions)

            totalPre[stock] = future_predictions.tolist()[0]
        print(totalPre)

        requests.get('http://127.0.0.1:5000/predictions', json=totalPre)

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
predictions()
