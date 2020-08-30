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
	return 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
