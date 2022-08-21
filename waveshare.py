from flask import Flask, render_template

from datetime import datetime

import requests
import json


# import sys
from weather_au import api

from weather_au import summary

app = Flask(__name__)

@app.route('/')
def index():




    dates={ 'day': datetime.now().day,
            'month': datetime.now().month,
            'year': datetime.now().year
    }

    # options = { method: 'GET', headers: { Accept: 'application/json' } };
    x = requests.get('https://beta.ourmanna.com/api/v1/get?format=json&order=daily')
    verse = json.loads(x.text)
    # print(verse['verse']['details'].keys())
    verse={ 'text': verse['verse']['details']['text'],
            'reference':  verse['verse']['details']['reference']
    }

    w = api.WeatherApi(search='strathfield+nsw', debug=0)
    print(w)
    location = w.location()

    print(f"\nLocation: {location['name']} {location['state']}, timezone:{location['timezone']}\n")

    for warn in w.warnings():
        print(f"Warning short title:  {warn['short_title']}")

        warning = w.warning(id=warn['id'])
        print(f"Warning title:        {warning['title']}")


    # print(f"\nObservations (temp): {observations['temp']:2}")
    # print(f"Forecast Rain:       amount:{forecast_rain['amount']}, chance:{forecast_rain['chance']}")

    # print('\n3 Hourly:')
    # for f in w.forecasts_3hourly():
        # print(f"{f['time']} temp:{f['temp']:2}, {f['icon_descriptor']}")

    # print(summary.Summary(search='strathfield+nsw'))

    observations = w.observations()
    forecast_rain = w.forecast_rain()
    weather = {'temp':observations['temp'],'rain':{'amount':{forecast_rain['amount']}, 'chance':{forecast_rain['chance']}}}

    return render_template('index.html', dates=dates, verse=verse, weather=weather)