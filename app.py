# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import flask
from flask import Flask, jsonify

app = Flask (__name__)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare (engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

@app.route("/")
def home():
    return (
        f"Welcome to Hawaii Precipitation Analysis"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>/<end>"
        )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    max_date = session.query (Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date (2017, 8, 23) - dt.timedelta (days=365)
    prcp_data = session.query (Measurement.date, Measurement.prcp).filter(Measurement.date > one_year_ago).all()
    precipitation_dict = dict(prcp_data)
    return jsonify(precipitation_dict)

@app.route ("/api/v1.0/stations")
def stations():
    number_of_stations = session.query (Measurement.station).distinct().count()
    stations_list = list(np.ravel(results_stations))
    return jsonify(stations_list)
    
@app.route("/api/v1.0/tobs")  
def tobs():
    tobs = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date>='2017,8,23').all
    tobs_list = list(np.ravel(tobs))
    return jsonify (tobs_list)
            
@app.route ("/api/v1.0/<start>/<end>")
def temps(start, end):
    temperature = [func.min(Measurement.tobs),
                   func.max(Measurement.tobs),
                   func.avg(Measurement.tobs)]
    session.query(*temperature).filter(Measurement.station=='USC00519281').all()
    return (jsonify ({"tempmin": min(found),"tempmax": max(found),"tempavg":np.mean}))

if __name__=="__main__": 
    app.run(debug=True)
    
        