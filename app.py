# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask
from flask import jsonify
import datetime as dt
import numpy as np


# create engine to hawaii.sqlite
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
      

app = Flask(__name__)

@app.route('/')
def index():
    # Find the most recent date in the data set.
    return (f"Welcome to the Hawaii Vacation App!<br/>"
            f"Available Routes:<br/>"
            f"Precipitation: /api/v1.0/precipitation <br/>"
            f"Stations: /api/v1.0/stations <br/>"
            f"Temperatures: /api/v1.0/tobs <br/>"
            f"Date Range:/api/v1.0/<start>/<end>"
           )
    

@app.route('/api/v1.0/precipitation')
def precipitation():
    earliest_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    rain_dates = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=earliest_date).all()
    precip = {date: prcp for date, prcp in rain_dates}
    return jsonify(precip)

@app.route('/api/v1.0/stations')
def station():
    station_names = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    station_names = [{
        'id': x[0],
        'name':x[1],
        'lat':x[2],
        'lng':x[3],
        'elev':x[4]
        } for x in station_names]
    return jsonify(station_names)

@app.route('/api/v1.0/tobs')
def tobs():
    earliest_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
                        order_by(func.count(Measurement.station).desc()).all()
    most_active = active_stations[0][0]
    recent_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=earliest_date)\
                .filter(Measurement.station==most_active).all()
    recent_temp = [{x[0]: x[1]} for x in recent_temp]
    return jsonify(recent_temp)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')          
def start(start=None, end=None):
    if not end:
        temp_range = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                    filter(Measurement.date>=start).all()
        temps = list(np.ravel(temp_range))
        return jsonify(temps)

    temp_range = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                   filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    temps=list(np.ravel(temp_range))
    return jsonify(temps=temps)
                               

if __name__ == "__main__":
    app.run(debug=True)
