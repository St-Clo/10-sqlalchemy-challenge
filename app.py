# flask app
import flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
# from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hawaii.sqlite'


engine = create_engine('sqlite:///hawaii.sqlite', connect_args={'check_same_thread': False})

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Database into ORM class
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# home / - list all available routes
@app.route("/")
def home():
    # return a list of all available api routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query for the dates and precipitation observations from the last year.
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date).all()

    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    prcp_dict = dict(results)

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query for the dates and temperature observations from the last year.
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        order_by(Measurement.date).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    tobs_dict = dict(results)

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    print(start)
    # Query for the dates and temperature observations from the last year.
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    print(results)

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    start_dict = {"min_temp": results[0][0], "max_temp": results[0][1], "avg_temp": results[0][2]}


    return jsonify(start_dict)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Query for the dates and temperature observations from the last year.
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    start_end_dict = {"min_temp": results[0][0], "max_temp": results[0][1], "avg_temp": results[0][2]}

    return jsonify(start_end_dict)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='
    