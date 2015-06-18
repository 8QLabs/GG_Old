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
    },context_instance=RequestContext(request))

def filter(request):
    lat = request.GET['lat']
    lon = request.GET['lon']

    print lat
    hits = get_taxi_data(lat, lon)

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

    return HttpResponse(json.dumps(data_array), content_type="application/json")

def get_tweets(lat, lon):
    result = es.search(index="tweets", doc_type="tweet", body={
        # "query": {"match_all" : { }},
        "query": {
            "filtered": {
                "filter": {
                    "geo_distance": {
                        "distance": "10km",
                        "location": {
                            "lat": lat,
                            "lon": lon
                        }
                    }
                }
            }
        },
        "size": 5000
    })

    hits = result['hits']['hits']

    return hits

def get_taxi_data(lat, lon):
    result = es.search(index="nyc_taxi_data", doc_type="taxi", body={
        # "query": {"match_all" : { }},
        "query": {
            "filtered": {
                "filter": {
                    "geo_distance": {
                        "distance": ".1km",
                        "dropoff_location": {
                            "lat": lat,
                            "lon": lon
                        }
                    }
                }
            }
        },
        "size": 10000
    })

    hits = result['hits']['hits']

    print str(len(hits)) + ' found'

    return hits