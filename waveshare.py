from flask import Flask, render_template

from datetime import datetime
import calendar
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

# bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = ''
with open('twitter.txt') as t_file:
    bearer_token = t_file.readline().strip()
    # print(bearer_token)

def create_url(list_id):
# Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=lang,author_id"
    # Be sure to replace list-id with any List ID
    # id = "list-id"
    url = "https://api.twitter.com/2/lists/{}/tweets".format(list_id)
    return url, tweet_fields




def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2ListLookupPython"
    return r


def connect_to_endpoint(url, list_fields):
    response = requests.request("GET", url, auth=bearer_oauth, params=list_fields)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()







app = Flask(__name__)

def nth(d):
    if d == 11 or d == 12 or d == 13:
        return 'th'

    elif d == 1:
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



    day = str(datetime.now().day) + nth(datetime.now().day)
    


    dates={ 'day': datetime.now().day,
            'nth': nth(datetime.now().day),
            'month': datetime.now().strftime("%b"),
            'year': datetime.now().year,
            'time': datetime.now().strftime("%H:%M")
    }
    # print(dates['time'])


    # options = { method: 'GET', headers: { Accept: 'application/json' } };
    x = requests.get('https://beta.ourmanna.com/api/v1/get?format=json&order=daily')
    verse = json.loads(x.text)
    # print(verse['verse']['details'].keys())
    verse={ 'text': verse['verse']['details']['text'],
            'reference':  verse['verse']['details']['reference']
    }

    w = api.WeatherApi(search='strathfield+nsw', debug=0)
    # print(w)
    location = w.location()

    obs = w.observations()
    today = w.forecasts_daily()[0]

    if today['temp_min'] is not None:
        weather = {
            'temp_now': today['now']['temp_now'],
            'rain_chance': today['rain']['chance'],
            'temp_min': today['temp_min'],
            'temp_max': today['temp_max'],
            'icon_descriptor': today['icon_descriptor'],
            'short_text':today['short_text'],
            'extended_text': today['extended_text']
        }
    else:
        weather = {
            'temp_now': today['now']['temp_now'],
            'rain_chance': today['rain']['chance'],
            'temp_min': today['now']['temp_now'],
            'temp_max': today['temp_max'],
            'icon_descriptor': today['icon_descriptor'],
            'short_text':today['short_text'],
            'extended_text': today['extended_text']
        }

    # print(weather)
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
        # print(e.begin.weekday())
        # print("Event '{}' starting {}".format(e.name, e.begin.humanize()))
        events.append({
            'name': e.name,
            'h_begin': e.begin.humanize(),
            'begin': calendar.day_name[e.begin.weekday()]
        })

    ## twitter
    waveshare_twitter_list_id = '1565329082333954048'
    url, list_fields = create_url(waveshare_twitter_list_id)
    json_response = connect_to_endpoint(url, list_fields)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    # print(json_response['data'][0])
    news = []
    for response in json_response['data']:
        # print(response)
        t = response['text'].split('http')[0][:140]
        if len(response['text'].split('http')[0]) > 139:
            t += '...'
        news.append(t)

    return render_template('index.html', dates=dates, verse=verse, weather=weather, events=events, len_events=len(events), news=news, len_news=len(news))

