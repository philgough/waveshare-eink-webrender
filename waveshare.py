from flask import Flask, render_template

from datetime import datetime

# url requests
import requests
import json


# weather
from weather_au import api









app = Flask(__name__)

def nth(d):
    if d == 1:
        return 'st'
    elif d == 2:
        return 'nd'
    elif d == 3:
        return 'rd'
    elif d > 3 and d < 21:
        return 'th'
    else:
        return 'th'



@app.route('/')
def index():



    day = str(datetime.now().day) + nth(datetime.now().day % 10)
    


    dates={ 'day': datetime.now().day,
            'nth': nth(datetime.now().day % 10),
            'month': datetime.now().strftime("%b"),
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

    obs = w.observations()
    today = w.forecasts_daily()[0]

    weather = {
        'temp_now': today['now']['temp_now'],
        'rain_chance': today['rain']['chance'],
        'temp_min': today['temp_min'],
        'temp_max': today['temp_max'],
        'icon_descriptor': today['icon_descriptor']
    }

    print(weather)

    return render_template('index.html', dates=dates, verse=verse, weather=weather)