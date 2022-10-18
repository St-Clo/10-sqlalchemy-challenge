import pandas as pd
import numpy as np
import datetime as dt
import os
import sqlalchemy
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, MetaData, inspect, func
from sqlalchemy import Column, Integer, String, Numeric, Text, Float
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.Measurement
Station = Base.classes.Station

session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Static Route
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and temperature observations from the last year."""
    precipitation = session.query(Measurement.date, func.avg(Measurement.tobs)).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
    group_by(Measurement.date).all()
    tobs_list = []
    for tobs in precipitation:
        tobs_dict = {}
        tobs_dict[tobs[0]] = round(tobs[1])
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    stations = session.query(Station.name).all()
    station_list = list(np.ravel(stations))
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a json list of Temperature Observations (tobs) for the previous year."""
    tobs = session.query(Measurement.tobs).\
    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    
    return jsonify(tobs)

#################################################
# SDynamic Route
#################################################
@app.route("/api/v1.0/<start>")
def start_temp(start):
    """Return a json list of the minimum temperature, the average temperature, 
    and the max temperature for a given start."""
    TMIN = session.query(func.min(Measurement.tobs)).\
           filter(Measurement.date == start).all()
    TMAX = session.query(func.max(Measurement.tobs)).\
           filter(Measurement.date == start).all()
    TAVG = session.query(func.avg(Measurement.tobs)).\
           filter(Measurement.date == start).all()
    result = TMIN, TMAX, TAVG
    temp_list = list(np.ravel(result))
    temp_dist = {'TMIN':temp_list[0], 'TMAX':temp_list[1], 'TAVG':temp_list[2]}
    
    return jsonify(temp_dist)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    """Return a json list of the minimum temperature, the average temperature,
    and the max temperature for a given start-end range."""
    TMIN = session.query(func.min(Measurement.tobs)).\
           filter(Measurement.date.between(start, end)).all()
    TMAX = session.query(func.max(Measurement.tobs)).\
           filter(Measurement.date.between(start, end)).all()
    TAVG = session.query(func.avg(Measurement.tobs)).\
           filter(Measurement.date.between(start, end)).all()
    result = TMIN, TMAX, TAVG
    temp_list = list(np.ravel(result))
    temp_dist = {'TMIN':temp_list[0], 'TMAX':temp_list[1], 'TAVG':temp_list[2]}
    
    return jsonify(temp_dist)

if __name__ == "__main__":
    app.run(debug=True)