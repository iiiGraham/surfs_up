# import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# import sql packages
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import flask
from flask import Flask, jsonify

# create engine to access sql file
engine = create_engine("sqlite:///hawaii.sqlite")

# set base function
Base = automap_base()

# reflect database file
Base.prepare(engine, reflect=True)

Base.classes.keys()

# initiate variables for table classes
Station = Base.classes.station
Measurement = Base.classes.measurement

# create session link to database
session = Session(engine)

# create flask instance
app = Flask(__name__)

# create flask root route
@app.route('/')
def welcome():
    return(
    '''Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    # set start date
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query precipitation data from dates - returned as list
    precipitation = session.query(Measurement.date, Measurement.prcp). \
    filter(Measurement.date >= prev_year).all()
    # create dictionary from list with comprehension
    precip = {date: prcp for date, prcp in precipitation}
    # return as json for web view
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    # ravel unpacks query into series which can be sent to list and then jsonified
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs). \
        filter(Measurement.station == 'USC00519281'). \
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))    
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel). \
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        jsonify(temps=temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
