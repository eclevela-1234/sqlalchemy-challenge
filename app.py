import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Database Path
# database_path = "Resources/hawaii.sqlite"

engine = create_engine("sqlite:///hawaii.sqlite")
# conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Assign the classes to respective variables called `Measurements` & 'Stations'
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
# write dict
    prcp_data = { date : prcp for date, prcp in results}
    print(prcp_data)

    return jsonify(prcp_data)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()
# write list
    station_data = list(np.ravel(results))
    

    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.tobs).all()

    session.close()
# write list
    temp_data = list(np.ravel(results))
    

    return jsonify(temp_data)

@app.route ("/api/v1.0/<start>")
@app.route ("/api/v1.0/<start>/<end>")
def query(start=None, end=None):
    session = Session(engine)
    if not end:
        results = session.query(func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date>= start).all()
        temps_list = list(np.ravel(results))
        return jsonify(temps_list)
    else:
        results = session.query(func.max(Measurement.tobs), func.avg(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date>= start).filter(Measurement.date<= end).all()
        temps_list = list(np.ravel(results))
        return jsonify(temps_list) 





if __name__ == '__main__':
    app.run(debug=True)
