from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from elasticsearch import Elasticsearch


# create instance of elasticsearch
es = Elasticsearch(["http://52.7.56.209:9200/"])

# Create your views here.
def map(request):

    result = es.search(index="tweets", doc_type="tweet", body={
        # "query": {"match_all" : { }},
        "query": {
            "filtered": {
                "filter": {
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
        "size": 1000
    })

    hits = result['hits']['hits']

    out = []

    for hit in hits:
        out.append(hit['_source']['location'])

    return render_to_response('core/mapbox.html', {
        'hits': out
    },context_instance=RequestContext(request))

def dashboard (request):
    return render_to_response('core/es_dashboard.html', {
    },context_instance=RequestContext(request))

def create_index (request):
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


