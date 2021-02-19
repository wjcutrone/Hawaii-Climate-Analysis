# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask
from flask import jsonify
import datetime as dt

def get_session():
    # create engine to hawaii.sqlite
    engine = create_engine("sqlite:///hawaii.sqlite")
    conn = engine.connect()

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # View all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

    # Create our session (link) from Python to the DB
    session = Session(engine)
    return session, Measurement, Station   

app = Flask(__name__)

@app.route('/api/v1.0/precipitation')
def precipitation():
    session, Measurement, Station = get_session()
    earliest_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    # Perform a query to retrieve the date and precipitation scores
    rain_dates = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=earliest_date).all()
    rain_dates = [{x[0]:x[1]} for x in rain_dates]
    return jsonify(rain_dates)

@app.route('/api/v1.0/stations')
def station():
    session, Measurement, Station = get_session()
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
    session, Measurement, Station = get_session()
    earliest_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
                        order_by(func.count(Measurement.station).desc()).all()
    most_active = active_stations[0][0]
    recent_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=earliest_date)\
                .filter(Measurement.station==most_active).all()
    recent_temp = [{x[0]: x[1]} for x in recent_temp]
    return jsonify(recent_temp)

# def start():
#     session, Measurement, Station = get_session()
#     # Get user's desired starting date
#     start_date = input('Please enter a start date (yyyy-mm-dd) no earlier than January 1st 2010')
#     start_date_requested = session.query(Measurement.date).filter(Measurement.date==start_date).first()
#     return jsonify(start_date_requested)

# @app.route('/api/v1.0/<start>/<end>')
# def end():
#     session, Measurement, Station = get_session()
#     #Get the user's desired end date
#     end_date = input("Please enter an end date (yyyy-mm-dd) up to August 23 2017")
#     end_date_requested = session.query(Measurement.date).filter(Measurement.date==end_date).first()
#     # Get temperature values for the users date range
#     temp_range = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs).\
#                    filter(Measurement.date>=start_date_requested).filter(Measurement.date<=end_date_requested).all()
#     return jsonify(temp_range)
                              
                               
    


@app.route('/')
def index():
    session, Measurement, Station = get_session()
    # Find the most recent date in the data set.
    return "Welcome to the Vacation App"
    
    

if __name__ == "__main__":
    app.run(debug=True)
