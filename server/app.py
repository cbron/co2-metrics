#!/usr/bin/env python

import json
import time

from flask import Flask, jsonify, Response
from flask_caching import Cache
from prometheus_client import Gauge, generate_latest
import co2meter as co2


app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# prom data
curr_co2 = Gauge('co2', 'Current CO2 level')
curr_temp = Gauge('temp', 'Current temperature in fahrenheit')

# get data from usb device
def grab_data():
	mon = co2.CO2monitor()
	data = mon.read_data() # 0 is time, 1 is co2, 2 is temp
	return {
		"co2": data[1],
		"temp": round(9 / 5 * data[2] + 32, 2),
	}

@app.route('/')
@cache.cached(timeout=30)
def json():
	return jsonify(grab_data())

@app.route('/metrics')
@cache.cached(timeout=30)
def metrics():
	data = grab_data()
	curr_co2.set(data["co2"])
	curr_temp.set(data["temp"])
	return Response(generate_latest(), mimetype='text/plain; version=0.0.4; charset=utf-8')

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')
