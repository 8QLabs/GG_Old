__author__ = 'rajiv'
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from elasticsearch import Elasticsearch

from django.conf import settings

consumer_key="1pHkCAf3Nuj9DSuPM9JYeC9CN"
consumer_secret= "mrsLgza7AIiADShBgkYxd5ippzG77ytuiiPnCgGvtY42MD6pq0"
access_token="535698855-JDY9iMbTPYQP0yXGYua2pVWS2m1VK2htMuUEyMfO"
access_token_secret= "27tfGAwjO6uKViTioi6lZbgEFnsI2btV5IsKBGRzYQqkB"

# create instance of elasticsearch
es = Elasticsearch(["http://localhost:9200/"])

# Bounding boxes for geolocations
# Online-Tool to create boxes (c+p as raw CSV): http://boundingbox.klokantech.com/
GEOBOX_WORLD = [-180,-90,180,90]
GEOBOX_NY = [-123.16, 36.2, -115.76, 39.52]

class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        # decode json
        if data is not None:
            print data
            tweet = json.loads(data)

        # pass tweet into TextBlob
        #tweet = TextBlob(dict_data["text"])

        # add text and sentiment info to elasticsearch
        if (tweet['text'] is not None and tweet['id'] is not None and tweet['created_at'] is not None and  tweet['user']['id'] is not None and  tweet['user']['name'] is not None and tweet['user']['followers_count'] is not None and tweet['user']['statuses_count'] is not None and tweet['user']['description'] is not None and tweet['coordinates'] is not None and tweet['coordinates'] is not 'null' ):
            es.index(index="tweets",
                 doc_type="tweet",
                 id=tweet["id"],
                 body={"timestamp_ms": tweet["timestamp_ms"],
                       "date_created": tweet["created_at"],
                       "user_id": tweet["user"]["id"],
                       "user_screen_name": tweet["user"]["screen_name"],
                       "user_name": tweet["user"]["name"],
                       "user_agent": tweet["source"],
                       "user_location": tweet["user"]["location"],
                       "followers_count": tweet["user"]["followers_count"],
                       "friends_count": tweet["user"]["friends_count"],
                       "location": {
                           "lat": tweet["coordinates"]["coordinates"][1],
                           "lon": tweet["coordinates"]["coordinates"][0]
                       },
                       "text": tweet["text"]
                 })
        return True

    # on failure
    def on_error(self, status):
        print status

if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for "congress" keyword
    stream.filter(locations=GEOBOX_NY )
