import arrow
import requests
from TwitterAPI import TwitterAPI

"""
Portland Air Quality bot. Data provided by aqicn.org.
"""

# Twitter stuff
consumer_key = '<twitter consumer key>'
consumer_secret = '<twitter consumer secret>'
access_token_key =  '<twitter access token key>'
access_token_secret = '<twitter access token secret>'

# aqicn.org stuff
api_token = '<aqicn.org API token>'
url = 'https://api.waqi.info/feed/geo:45.516483;-122.617294/'
params = {'token': api_token}

# PM 2.5 AQI ranges
good = range(0, 51)
moderate = range(51, 101)
unhealthy_for_sensitive_groups = range(101, 151)
unhealthy = range(151, 201)
very_unhealthy = range(201, 301)
hazardous = range(301, 1001)

def get_aqi_data():
    r = requests.get(url, params=params)
    resp = r.json()
    return (resp['data']['aqi'], resp['data']['time']['s'])


def infer_health(aqi):
    if aqi in good:
        return 'good'
    elif aqi in moderate:
        return 'moderate'
    elif aqi in unhealthy_for_sensitive_groups:
        return 'unhealthy for sensitive groups'
    elif aqi in unhealthy:
        return 'unhealthy'
    elif aqi in very_unhealthy:
        return 'very unhealthy'
    elif aqi in hazardous:
        return 'hazardous'
    else:
        return 'unknown'

def main():
    # Make request to aqicn.org
    aqi, ts = get_aqi_data()
    t = arrow.get(ts)
    stat_msg = 'Portland PM2.5 AQI is {0} as of {1} at {2}.\n' \
        .format(aqi, t.strftime('%m/%d/%y'), t.strftime('%I:%M%p'))
    health_str = infer_health(aqi)
    health_msg = 'Air quality is {0}.'.format(health_str)

    # Tweet the info
    twitter = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    tweet = stat_msg + '' + health_msg
    twitter.request('statuses/update', {'status': tweet})
    print(tweet)


if __name__ == '__main__':
    main()
