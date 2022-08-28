from flask import Flask, render_template

from datetime import datetime

# url requests
import requests
import json


# weather
from weather_au import api



from ics import Calendar 
import requests

def cal_from_file(filename: str, prodid: str = 'PRODID:-//placeholder//text//EN\n') -> Calendar:
    buf = []

    with open(filename, 'r') as f:
        i = 0
        vcal = -1
        missing_prodid = True

        for line in f:
            buf.append(line)

            if line == "BEGIN:VCALENDAR\n":
                vcal = i
                missing_prodid = True
            elif line == "END:VCALENDAR\n":
                if missing_prodid:
                    #print(f'VCALENDAR without PRODID on line {vcal} in {filename}.')
                    buf[vcal] = buf[vcal] + prodid
                vcal = -2
            elif vcal != -1 and missing_prodid and line.startswith("PRODID:"):
                missing_prodid = False
            i += 1

        if vcal == -1:
            raise TypeError(f'{filename} is not an ics file') # FIXME
        elif vcal >= 0 and missing_prodid:
            #print(f'VCALENDAR without PRODID nor end on line {vcal} in {filename}.')
            buf[vcal] = buf[vcal] + prodid

    return Calendar(''.join(buf))







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
    url =''
    with open('cal_url.txt', 'r') as f:
        url=f.readline().strip()
    # print(url)
    response = requests.get(url)
    open("cal.ics", "wb").write(response.content)
    # print(cal_from_file('cal.ics'))
    cal = cal_from_file('cal.ics')
    # print(cal.events)

    events = []
    for e in list(cal.timeline.start_after(datetime.now().astimezone())):
        print("Event '{}' starting {}".format(e.name, e.begin.humanize()))
        events.append({
            'name': e.name,
            'h_begin': e.begin.humanize()
        })
    return render_template('index.html', dates=dates, verse=verse, weather=weather, events=events, len_events=len(events))

