import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify
import numpy as np
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# ## Hints
# * You will need to join the station and measurement tables for some of the queries.
# * Use Flask `jsonify` to convert your API data into a valid JSON response object.
app = Flask(__name__)

# * `/`
#   * Home page.
#   * List all routes that are available.
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipition<br/>"
        f"/api/v1.0/station <br/>"
        f"/api/v1.0/tobs </br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end></br>"
    )

# * `/api/v1.0/precipitation`
#   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session= Session(engine)
    sel= [Measurement.date, Measurement.prcp]
    prcp_data = session.query(*sel).all()
    session.close()
    precipitation = []
    for date, prcp in prcp_data:
        dictionary = {}
        dictionary["date"] = date
        dictionary["prcp"] = prcp
        precipitation.append(dictionary)
    return jsonify(precipitation)

# * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()
    station_list = list(np.ravel(stations))
    return jsonify(station_list)
    
# * `/api/v1.0/tobs`
#   * Query the dates and temperature observations of the most active station for the last year of data.
#   * Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    dates = dt.date(2017, 8, 23) - dt.timedelta(weeks=52)
    station_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").\
    filter(Measurement.date >= dates).order_by(Measurement.date.desc()).all()
    session.close()
    tobs_list = list(np.ravel(station_temp))
    return jsonify(tobs_list)

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def start_dates(start):
    session = Session(engine)
    start_result = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    session.close()
    tobs_start_end = list(np.ravel(start_result))
    return jsonify(tobs_start_end)

@app.route ("/api/v1.0/<start>/<end>")
def start_end_dates (start, end):
    session = Session(engine)
    star_end_result = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date > start).filter(Measurment.date < end).all()
    session.close()
    tobs_start_end = list(np.ravel(star_end_result))
    return jsonify(tobs_start_end)

if __name__ =="__main__":
        app.run(debug=True)