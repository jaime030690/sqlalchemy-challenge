# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Setup flask
app = Flask(__name__)

# Pull last date
session = Session(engine)

# Query to pull last date
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
session.close()

# Flask routes
@app.route('/')
def home():
    return (
        f'<h1>Climate App API</h1><hr>'
        f'<h2>Available Routes</h2>'
        f'/api/v1.0/precipitation<br>'
        f'/api/v1.0/stations<br>'
        f'/api/v1.0/tobs<br>'
        f'/api/v1.0/start<br>'
        f'/api/v1.0/start/end'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():

    # Setup session
    session = Session(engine)

    # Query to pull date and prcp
    prcp_query = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Will return this
    prcp_results = []
    
    # Look thru query, use date as key and prcp as value, and add dict to list
    for d, p in prcp_query:
        climate_dict = {}
        climate_dict[d] = p
        prcp_results.append(climate_dict)

    return jsonify(prcp_results)

@app.route('/api/v1.0/stations')
def stations():

    # Setup engine
    session = Session(engine)

    # Query to pull station and name
    stations_query = session.query(Station.station, Station.name).all()
    session.close()

    # Will return this
    stations_results = []

    # Look thru query, use station and name as keys and apply the corresponding values, add to list
    for s, n in stations_query:
        station_dict = {}
        station_dict['station'] = s
        station_dict['name'] = n
        stations_results.append(station_dict)

    return jsonify(stations_results)

@app.route('/api/v1.0/tobs')
def tobs():

    # Setup engine
    session = Session(engine)

    # Calculate date for one year ago
    y, m, d = [int(item) for item in last_date.split("-")]
    cutoff = dt.datetime(y-1, m, d)

    # Query to pull tobs
    tobs_query = session.query(Measurement.tobs).filter(func.strftime(Measurement.date) >= cutoff).all()
    session.close()

    # Return this
    tobs_results = []

    # Convert query to a list
    tobs_results = list(np.ravel(tobs_query))

    return jsonify(tobs_results)
    
@app.route('/api/v1.0/<start>')
def start(start):

    # Get query
    start_query = calc_temps(start, last_date)

    # Return this
    start_results = []
    
    # Convert query to a list
    start_results = list(np.ravel(start_query))
    
    return jsonify(start_results)
    

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):

    # Get query
    start_end_query = calc_temps(start, end)

    # Return this
    start_end_results = []

    # Convert query to a list
    start_end_results = list(np.ravel(start_end_query))

    return jsonify(start_end_results)

def calc_temps(start_date, end_date):
    
    # Setup engine
    session = Session(engine)
    
    # Query to get temperature stats
    stats_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    return stats_query

if __name__ == '__main__':
    app.run(debug=True)