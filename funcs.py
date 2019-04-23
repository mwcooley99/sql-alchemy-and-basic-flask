from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import datetime as dt

# Set up Models
# engine = create_engine('sqlite:///Instructions/Resources/hawaii.sqlite')
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Create the Base and models
# Base = automap_base()
# Base.prepare(engine, reflect=True)
#
# Measurement = Base.classes.measurement
# Station = Base.classes.station

# Get the most recent date
most_recent_date, =  session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Get the date one year prior to the most_recent date and convert it to the same format
start_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(weeks=52)
start_date = start_date.strftime('%Y-%m-%d')

# Get the precipitation data
def prcp_query(start_date=start_date, end_date=most_recent_date):
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= start_date, Measurement.date <=end_date)\
        .order_by(Measurement.date).all()
    return [{k: v} for k, v in precipitation_data]

print(prcp_query())



