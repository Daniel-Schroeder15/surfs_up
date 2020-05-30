# import the Flask dependency
from flask import Flask

# create a new Flask app instance
# __name__ is a magic method
app = Flask(__name__)


# create routes
# the starting route is the root
@app.route('/')
def hello_world():
	return 'Hello world'

@app.route('/name')
def names():
    name = "Daniel"
    return f'Hello world, my name is {name}'
