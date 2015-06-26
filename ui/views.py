from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse
import json

from elasticsearch import Elasticsearch

# create instance of elasticsearch
es = Elasticsearch([settings.ELASTIC_SEARCH_HOST])

# Create your views here.
def index(request):
    return render_to_response('ui/index.html', {
    },context_instance=RequestContext(request))

# Create your views here.
def map(request):

    return render_to_response('mapbox.html', {
        'start_lat': 40.7611095,
        'start_lon': -73.9913995
    },context_instance=RequestContext(request))

def filter(request):
    lat = request.GET['lat']
    lon = request.GET['lon']

    data_array = None
    if request.GET['index'] == 'taxi':
        data_array = filter_taxi_data(lat, lon, request)
    elif request.GET['index'] == 'tweets':
        data_array = filter_tweets(lat, lon, request)

    return HttpResponse(json.dumps(data_array), content_type="application/json")

def filter_taxi_data (lat, lon, request):
    query_filter = [{
        "geo_distance": {
            "distance": ".1km",
            "dropoff_location": {
                "lat": lat,
                "lon": lon
            }
        }
    }]

    extra_filters = build_time_filter(request)
    query_filter.extend(extra_filters)

    result = es.search(index="nyc_taxi_data", doc_type="taxi", body={
        # "query": {"match_all" : { }},
        "query": {
            "filtered": {
                "filter": {
                    "and" : query_filter
                }
            }
        },
        "size": 10000
    })

    hits = result['hits']['hits']

    print str(len(hits)) + ' pick locations found.'

    data_array = []
    for hit in hits:
        hit_lat = hit['_source']['pickup_location']['lat']
        hit_lon = hit['_source']['pickup_location']['lon']
        data_array.append({
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [hit_lon, hit_lat]
            },
            "properties": {
                "marker-color": "dodgerblue",
                "marker-size": "small",
                "icon": {
                    "className": "css-icon"
                }
            }
         })

    return data_array

def build_time_filter(request):
    query_filter = []
    if 'time_of_day' in request.GET:
        time_of_day = request.GET['time_of_day']

        if time_of_day != '-1':
            if time_of_day == 'Morning':
                query_filter.append({
                    "range" : {
                        "hour_of_day" : {
                            "gte" : "8",
                            "lt" : "12"
                        }
                    }
                })
            elif time_of_day == 'Afternoon':
                query_filter.append({
                    "range" : {
                        "hour_of_day" : {
                            "gte" : "12",
                            "lt" : "17"
                        }
                    }
                })
            elif time_of_day == 'Evening':
                query_filter.append({
                    "range" : {
                        "hour_of_day" : {
                            "gte" : "17",
                            "lt" : "23"
                        }
                    }
                })
            elif time_of_day == 'Night':
                query_filter.append({
                    "range" : {
                        "hour_of_day" : {
                            "gte" : "0",
                            "lt" : "8"
                        }
                    }
                })

    if 'time_of_week' in request.GET:
        time_of_week = request.GET['time_of_week']
        if time_of_week != '-1':
            if time_of_week == 'Weekday':
                query_filter.append({
                    "terms" : {
                        "weekday" : [0,1,2,3,4]
                    }
                })
            elif time_of_week == 'Weekend':
                query_filter.append({
                    "terms" : {
                        "weekday" : [5, 6]
                    }
                })

    return query_filter

def filter_tweets(lat, lon, request):
    query_filter = [{
        "geo_distance": {
            "distance": "10km",
            "location": {
                "lat": lat,
                "lon": lon
            }
        }
    }]

    extra_filters = build_time_filter(request)
    query_filter.extend(extra_filters)

    result = es.search(index="tweets", doc_type="tweet", body={
        # "query": {"match_all" : { }},
        "query": {
            "filtered": {
                "filter": query_filter
            }
        },
        "size": 5000
    })

    hits = result['hits']['hits']

    return hits