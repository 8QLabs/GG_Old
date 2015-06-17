from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from elasticsearch import Elasticsearch

# create instance of elasticsearch
es = Elasticsearch([settings.ELASTIC_SEARCH_HOST])

# Create your views here.
def index(request):
    return render_to_response('ui/index.html', {
    },context_instance=RequestContext(request))

# Create your views here.
def map(request):
    out = get_taxi_data()

    return render_to_response('mapbox.html', {
        'hits': out
    },context_instance=RequestContext(request))

def get_tweets():
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

    return out

def get_taxi_data():
    result = es.search(index="nyc_taxi_data", doc_type="taxi", body={
        # "query": {"match_all" : { }},
        "query": {
            "filtered": {
                "filter": {
                    "geo_distance": {
                        "distance": "4km",
                        "dropoff_location": {
                            "lat": 40.7611095,
                            "lon": -73.9913995
                        }
                    }
                }
            }
        },
        "size": 3000
    })

    hits = result['hits']['hits']

    out = []

    for hit in hits:
        out.append(hit['_source']['dropoff_location'])

    return out