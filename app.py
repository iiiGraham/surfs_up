# import dependencies
from flask import Flask

# create flask instance
app = Flask(__name__)

# create flask root route
@app.route('/')
# create function for the route
def hello_world():
    return "Hello World"

# create route
@app.route('/new_page')
def say_something():
    return "something <]:)"