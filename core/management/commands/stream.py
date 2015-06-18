__author__ = 'rajiv'
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from elasticsearch import Elasticsearch
import csv
import sys

from datetime import date

from django.conf import settings

consumer_key="1pHkCAf3Nuj9DSuPM9JYeC9CN"
consumer_secret= "mrsLgza7AIiADShBgkYxd5ippzG77ytuiiPnCgGvtY42MD6pq0"
access_token="535698855-JDY9iMbTPYQP0yXGYua2pVWS2m1VK2htMuUEyMfO"
access_token_secret= "27tfGAwjO6uKViTioi6lZbgEFnsI2btV5IsKBGRzYQqkB"

# create instance of elasticsearch
# es = Elasticsearch(["http://localhost:9200/"])

# Bounding boxes for geolocations
# Online-Tool to create boxes (c+p as raw CSV): http://boundingbox.klokantech.com/

#southwest corner then north east
GEOBOX_WORLD = [-180,-90,180,90]
GEOBOX_NY = [-78.57, 36.54, -68.74, 43.78]
GEOBOX_CA = [-123.16, 39.52, -115.76, 32.6]
GEOBOX_SF = [-122.5777, 37.1803, -121.7216, 38.0164]

FILE_DIR = '/mnt/data/twitter/'

FILE_OUT = None
TODAY_DATE_STR = ''
CITY = sys.argv[1]

def get_file_writer():
    global TODAY_DATE_STR
    global FILE_OUT

    current_date_str = date.today().strftime("%m-%d-%Y")

    if TODAY_DATE_STR != current_date_str:
        TODAY_DATE_STR = current_date_str
        filename = FILE_DIR + 'twitter_' + CITY + '_' + current_date_str + '.txt'

        if FILE_OUT:
            FILE_OUT.close()

        FILE_OUT = open(filename, 'w')

    return FILE_OUT

def valid(data):
    if data and data is not None:
        return True

class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        # decode json
        if data is not None:
            tweet = json.loads(data)

            # add text and sentiment info to elasticsearch
            if (valid(tweet['text'])
                and valid(tweet['id'])
                and valid(tweet['created_at'])
                and valid(tweet['user']['id'])
                and valid(tweet['user']['name'])
                and valid(tweet['user']['followers_count'])
                and valid(tweet['user']['statuses_count'])
                and valid(tweet['user']['description'])
                and valid(tweet['coordinates'])
                and tweet['coordinates'] is not 'null'):

                writer = get_file_writer()
                print data
                FILE_OUT.write(data)

        return True

    # on failure
    def on_error(self, status):
        print status


# to_write = {"timestamp_ms": tweet["timestamp_ms"],
#                    "date_created": tweet["created_at"],
#                    "user_id": tweet["user"]["id"],
#                    "user_screen_name": tweet["user"]["screen_name"],
#                    "user_name": tweet["user"]["name"],
#                    "user_agent": tweet["source"],
#                    "user_location": tweet["user"]["location"],
#                    "followers_count": tweet["user"]["followers_count"],
#                    "friends_count": tweet["user"]["friends_count"],
#                    "location": {
#                        "lat": tweet["coordinates"]["coordinates"][1],
#                        "lon": tweet["coordinates"]["coordinates"][0]
#                    },
#                    "text": tweet["text"]
#              }

def index_tweet():
    pass
    # es.index(index="tweets",
    #      doc_type="tweet",
    #      id=tweet["id"],
    #      body={"timestamp_ms": tweet["timestamp_ms"],
    #            "date_created": tweet["created_at"],
    #            "user_id": tweet["user"]["id"],
    #            "user_screen_name": tweet["user"]["screen_name"],
    #            "user_name": tweet["user"]["name"],
    #            "user_agent": tweet["source"],
    #            "user_location": tweet["user"]["location"],
    #            "followers_count": tweet["user"]["followers_count"],
    #            "friends_count": tweet["user"]["friends_count"],
    #            "location": {
    #                "lat": tweet["coordinates"]["coordinates"][1],
    #                "lon": tweet["coordinates"]["coordinates"][0]
    #            },
    #            "text": tweet["text"]
    #      })

if __name__ == '__main__':
    geo = None
    if CITY == 'ca':
        geo = GEOBOX_CA
    elif CITY == 'sf':
        geo = GEOBOX_SF
    elif CITY == 'ny':
        geo = GEOBOX_NY
    else:
        geo = GEOBOX_NY

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)



    # search twitter for "congress" keyword
    stream.filter(locations=geo )