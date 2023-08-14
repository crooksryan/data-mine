from flask import Flask, render_template

app = Flask(__name__)

# get sql db for each stock

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictions')
def predictions():
    # functions will handle making changes to the db
    ...

app.run('0.0.0.0', debug=True)