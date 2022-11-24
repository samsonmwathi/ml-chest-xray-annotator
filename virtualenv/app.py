from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('landing.html')

@app.route('/signup/')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('main.html')

