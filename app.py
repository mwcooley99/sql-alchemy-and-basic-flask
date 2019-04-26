import os
from flask import Flask, jsonify, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.automap import automap_base

import datetime as dt

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'hawaii.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Add extensions to the app
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

# Create the Base
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Create the Models
Measurement = Base.classes.measurement
Station = Base.classes.station


@app.route('/')
def index():
    '''Home page'''
    return render_template('index.html')


@app.route('/api/v1.0/precipitation')
def precipitation():
    precipitation_data = db.session.query(Measurement.date,
                                          Measurement.prcp).all()
    return jsonify([{k: v} for k, v in precipitation_data])


@app.route('/api/v1.0/stations')
def stations():
    stations = [s.__dict__ for s in db.session.query(Station).all()]
    for station in stations:
        station.pop('_sa_instance_state', None)

    return jsonify(stations)


@app.route('/api/v1.0/tobs')
def tobs():
    # Find the last data point
    most_recent_date, = db.session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()

    # Get the start date
    start_date = dt.datetime.strptime(most_recent_date,
                                      "%Y-%m-%d") - dt.timedelta(weeks=52)
    start_date = start_date.strftime('%Y-%m-%d')

    # Query the data
    precipitation_data = db.session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.date >= start_date,
                Measurement.date <= most_recent_date) \
        .order_by(Measurement.date).all()
    return jsonify([{k: v} for k, v in precipitation_data])


@app.route('/api/v1.0/<start>')
def stats_from_start(start):
    query = db.session.query(db.func.min(Measurement.tobs),
                             db.func.avg(Measurement.tobs),
                             db.func.max(Measurement.tobs)).filter(
        Measurement.date >= start).first()
    keys = ['TMIN', 'TAVG', 'TMAX']

    return jsonify(dict(zip(keys, query)))


@app.route('/api/v1.0/<start>/<end>')
def stats_from_start_end(start, end):
    query = db.session.query(db.func.min(Measurement.tobs),
                             db.func.avg(Measurement.tobs),
                             db.func.max(Measurement.tobs)).filter(
        Measurement.date >= start, Measurement.date <= end).first()

    keys = ['TMIN', 'TAVG', 'TMAX']

    return jsonify(dict(zip(keys, query)))


if __name__ == "__main__":
    app.run(debug=True)
