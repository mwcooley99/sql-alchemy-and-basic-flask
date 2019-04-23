import os

from flask import Flask, jsonify, render_template

from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session

import datetime as dt

# from funcs import prcp_query

# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Set up Models
engine = create_engine('sqlite:///Instructions/Resources/hawaii.sqlite')
Session = sessionmaker(bind=engine)
session = scoped_session(Session)

# Create the Base and models
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

most_recent_date, =  session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Get the date one year prior to the most_recent date and convert it to the same format
start_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(weeks=52)
start_date = start_date.strftime('%Y-%m-%d')

@app.route('/')
def index():
    '''Home page'''
    return render_template('index.html')

@app.route('/api/v1.0/precipitation')
def precipitation():
    precipitation_data = session.query(Measurement.date, Measurement.prcp) \
        .filter(Measurement.date >= start_date, Measurement.date <= most_recent_date) \
        .order_by(Measurement.date).all()
    return jsonify([{k: v} for k, v in precipitation_data])

@app.route('/api/v1.0/stations')
def stations():
    stations = [s.__dict__ for s in  session.query(Station).all()]
    for station in stations: station.pop('_sa_instance_state', None)
    print(stations)
    return jsonify(stations)


if __name__ == "__main__":
    app.run(debug=True)

