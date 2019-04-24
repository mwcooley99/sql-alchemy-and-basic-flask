import os

from flask import Flask, jsonify, render_template

from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session

from flask_bootstrap import Bootstrap

import datetime as dt

app = Flask(__name__)
bootstrap = Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# Set up Models
engine = create_engine('sqlite:///hawaii.sqlite')
Session = sessionmaker(bind=engine)
session = scoped_session(Session)


# Create the Base and models
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


@app.route('/')
def index():
    '''Home page'''
    return render_template('index.html')


@app.route('/api/v1.0/precipitation')
def precipitation():
    precipitation_data = session.query(Measurement.date,
                                       Measurement.prcp).all()
    return jsonify([{k: v} for k, v in precipitation_data])


@app.route('/api/v1.0/stations')
def stations():
    stations = [s.__dict__ for s in session.query(Station).all()]
    for station in stations: station.pop('_sa_instance_state', None)

    return jsonify(stations)


@app.route('/api/v1.0/tobs')
def tobs():
    # Find the last data point
    most_recent_date, = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()

    # Get the start date
    start_date = dt.datetime.strptime(most_recent_date,
                                      "%Y-%m-%d") - dt.timedelta(weeks=52)
    start_date = start_date.strftime('%Y-%m-%d')

    # Query the data
    precipitation_data = session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.date >= start_date,
                Measurement.date <= most_recent_date) \
        .order_by(Measurement.date).all()
    return jsonify([{k: v} for k, v in precipitation_data])


@app.route('/api/v1.0/<start>')
def stats_from_start(start):
    query = session.query(func.min(Measurement.tobs),
                          func.avg(Measurement.tobs),
                          func.max(Measurement.tobs)).filter(
        Measurement.date >= start).first()
    keys = ['TMIN', 'TAVG', 'TMAX']

    return jsonify(dict(zip(keys, query)))


@app.route('/api/v1.0/<start>/<end>')
def stats_from_start_end(start, end):
    query = session.query(func.min(Measurement.tobs),
                          func.avg(Measurement.tobs),
                          func.max(Measurement.tobs)).filter(
        Measurement.date >= start, Measurement.date <= end).first()

    keys = ['TMIN', 'TAVG', 'TMAX']

    return jsonify(dict(zip(keys, query)))


if __name__ == "__main__":
    app.run(debug=True)
