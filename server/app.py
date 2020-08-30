#!/usr/bin/env python

from flask import Flask, jsonify
from flask_caching import Cache
import json
import time
import co2meter as co2

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

def grab_data():
	response = {}
	try:
		mon = co2.CO2monitor()
		data = mon.read_data()
		response = {
			"time": time.mktime(data.index[0].timetuple()),
			"co2": data["co2"],
			"temp": data["temp"],
		}
	except:
		response = {
			"status": "failure"
		}
	return response


@app.route('/')
@cache.cached(timeout=30)
def json():
	return jsonify(grab_data())

@app.route('/metrics')
@cache.cached(timeout=30)
def metrics():
	return 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
