from flask import Flask, render_template, request
from dotenv.main import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from time import sleep

from stockAPI import StockAPI

app = Flask(__name__)

load_dotenv()
DBuser = os.getenv('DBuser')
DBpassword = os.getenv('DBpassword')

if DBuser is None or DBpassword is None:
    raise KeyError

os.environ['DATABASE_URL'] = f'postgresql://{DBuser}:{DBpassword}@localhost/data-mine'

if not os.environ['DATABASE_URL']:
    raise RuntimeError('db bad')

engine = create_engine(os.environ['DATABASE_URL'])
db = scoped_session(sessionmaker(bind=engine))

api = StockAPI()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictions')
def predictions():
    # functions will handle making changes to the db
    data = request.get_json()

    for stock in api.stocks:
        pred = data.get(stock, None)

        if pred is None:
            print(f'NO PREDICTION FOR {stock}')
            continue
        try:
            price = api.get_bars([stock])[stock.upper()].vw
        except Exception:
            sleep(30)
            price = api.get_bars([stock])[stock.upper()].vw

        if price <= pred[0]:
            # buy
            ...
        elif price > pred[0]:
            # sell
            ...
        else:
            # hold
            ...

    return "200"


app.run('0.0.0.0', port=5000, debug=True)
