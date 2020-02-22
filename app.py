# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Setup flask
app = Flask(__name__)

# Flask routes
@app.route('/')
def home():
    return (
        f'<h1>Climate App API</h1><hr>'
        f'<h2>Available Routes</h2>'
        f'/api/v1.0/precipitation<br>'
        f'/api/v1.0/stations<br>'
        f'/api/v1.0/tobs<br>'
        f'/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():

    ''' 
    TODO:
    Convert the query results to a Dictionary using date as the key and prcp as the value.
    Return the JSON representation of your dictionary.

    '''

@app.route('/api/v1.0/stations')
def stations():

    '''
    TODO:
    Return a JSON list of stations from the dataset.

    '''

@app.route('/api/v1.0/tobs')
def tobs():

    '''
    TODO:
    Query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year.
    
    '''

@app.route('/api/v1.0/<start>')
def start(start):

    '''
    TODO:
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

    '''

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):

    '''
    TODO:
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

    '''
    
if __name__ == '__main__':
    app.run(debug=True)