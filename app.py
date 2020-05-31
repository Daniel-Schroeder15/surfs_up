# import the Flask dependency
from flask import Flask, jsonify

# import denpendencies
import datetime as dt
import numpy as np
import pandas as pd

#import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# obtain access to database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# create a new Flask app instance
# __name__ is a magic method
app = Flask(__name__)


# create routes
# the starting route is the root
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():    

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    session.close()
    return jsonify(precip)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations)


# monthly temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps)
# convert to a list and jsonify the list
# the .\  is used to signify that we want our query to continue on the next line.


# statistics route 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# calcutlate the temperate minimum, average, and maximum
def stats(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)



# def hello_world():
# 	return 'Hello world'

# @app.route('/name')
# def names():
#     name = "Daniel"
#     return f'Hello world, my name is {name}'
if __name__ =="__main__":
    app.run(debug=True)