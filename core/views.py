from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from elasticsearch import Elasticsearch
import tweepy
import time
import csv

# create instance of elasticsearch
es = Elasticsearch([settings.ELASTIC_SEARCH_HOST])

# Create your views here.
def map(request):
    result = es.search(index="tweets", doc_type="tweet", body={
        # "query": {"match_all" : { }},
        "query": {
            "filtered": {
                "filter": {
                    "geo_distance": {
                        "distance": "10km",
                        "location": {
                            "lat": 40.7611095,
                            "lon": -73.9913995
                        }
                    }
                }
            }
        },
        "size": 5000
    })

    hits = result['hits']['hits']

    out = []

    for hit in hits:
        out.append(hit['_source']['location'])

    return render_to_response('core/mapbox.html', {
        'hits': out
    },context_instance=RequestContext(request))

def filter_data_on_map (request):
    if request.method == 'GET':
        result = es.search(index="tweets", doc_type="tweet", body={
            # "query": {"match_all" : { }},
            "query": {
                "filtered": {
                    "filter": {
                        "and" : [
                            {
                                "range" : {
                                    "postDate" : {
                                        "from" : "2010-03-01",
                                        "to" : "2010-04-01"
                                    }
                                }
                            },
                            {
                                "prefix" : { "name.second" : "ba" }
                            }
                        ],
                        "geo_distance": {
                            "distance": "1.5km",
                            "location": {
                                "lat": 40.7611095,
                                "lon": -73.9913995
                            }
                        }
                    }
                }
            },
            "size": 500
        })

        hits = result['hits']['hits']

        out = []

        for hit in hits:
            out.append(hit['_source']['location'])

        return render_to_response('core/mapbox.html', {
            'hits': out
        },context_instance=RequestContext(request))


def pull_historical_tweets(request):
    auth = tweepy.OAuthHandler('1pHkCAf3Nuj9DSuPM9JYeC9CN', 'mrsLgza7AIiADShBgkYxd5ippzG77ytuiiPnCgGvtY42MD6pq0')
    auth.set_access_token('535698855-JDY9iMbTPYQP0yXGYua2pVWS2m1VK2htMuUEyMfO', '27tfGAwjO6uKViTioi6lZbgEFnsI2btV5IsKBGRzYQqkB')
    api = tweepy.API(auth)

    lat = '40.7611095'
    lon = '-73.9913995'
    c = tweepy.Cursor(api.search, q='', count='100', geocode=lat+','+lon+','+'5mi').items()
    localtweets = []
    while True:
        try:
            tweet = c.next()
            print tweet
            # localtweets.append({
            #     'text':tweet.text.encode('utf8', 'ignore'),
            #     'date':tweet.created_at,
            #     'id':tweet.author._json['id'],
            #     'name':tweet.author._json['name'].encode('utf8', 'ignore'),
            #     'followers_count':tweet.author._json['followers_count'],
            #     'statuses_count':tweet.author._json['statuses_count'],
            #     'description':tweet.author._json['description'].encode('utf8', 'ignore'),
            #     # 'tract':tract,
            #     'slat':lat,
            #     'slon':lon,
            #     'lat':tweet._json['coordinates']['coordinates'][1],
            #     'lon':tweet._json['coordinates']['coordinates'][0],
            #     'tweet_id':tweet.id
            # })
        except tweepy.TweepError:
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break

    return render_to_response('core/es_dashboard.html', {
    },context_instance=RequestContext(request))

def dashboard (request):
    return render_to_response('core/es_dashboard.html', {
    },context_instance=RequestContext(request))

def create_taxi_index (request):
    es.indices.create(index='taxis', body={
        "mappings":{
            "tweet":{
                "properties":{
                    "date_created":{
                        "type":"string"
                    },
                    "followers_count":{
                        "type":"long"
                    },
                    "friends_count":{
                        "type":"long"
                    },
                    "location": {
                        "type": "geo_point"
                    },
                    "text":{
                        "type":"string"
                    },
                    "timestamp_ms":{
                        "type":"long"
                    },
                    "user_agent":{
                        "type":"string"
                    },
                    "user_id":{
                        "type":"long"
                    },
                    "user_location":{
                        "type":"string"
                    },
                    "user_name":{
                        "type":"string"
                    },
                    "user_screen_name":{
                        "type":"string"
                    }
                }
            }
        }
    })

def create_tweet_index (request):
    es.indices.create(index='tweets', body={
        "mappings":{
            "tweet":{
                "properties":{
                    "date_created":{
                        "type":"string"
                    },
                    "followers_count":{
                        "type":"long"
                    },
                    "friends_count":{
                        "type":"long"
                    },
                    "location": {
                        "type": "geo_point"
                    },
                    "text":{
                        "type":"string"
                    },
                    "timestamp_ms":{
                        "type":"long"
                    },
                    "user_agent":{
                        "type":"string"
                    },
                    "user_id":{
                        "type":"long"
                    },
                    "user_location":{
                        "type":"string"
                    },
                    "user_name":{
                        "type":"string"
                    },
                    "user_screen_name":{
                        "type":"string"
                    }
                }
            }
        }
    })

    return render_to_response('core/es_dashboard.html', {
    },context_instance=RequestContext(request))


