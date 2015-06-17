from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from elasticsearch import Elasticsearch
import tweepy
import time
import csv


def dashboard (request):
    return render_to_response('core/es_dashboard.html', {
    },context_instance=RequestContext(request))


# def create_tweet_index (request):
#     es.indices.create(index='tweets', body={
#         "mappings":{
#             "tweet":{
#                 "properties":{
#                     "date_created":{
#                         "type":"string"
#                     },
#                     "followers_count":{
#                         "type":"long"
#                     },
#                     "friends_count":{
#                         "type":"long"
#                     },
#                     "location": {
#                         "type": "geo_point"
#                     },
#                     "text":{
#                         "type":"string"
#                     },
#                     "timestamp_ms":{
#                         "type":"long"
#                     },
#                     "user_agent":{
#                         "type":"string"
#                     },
#                     "user_id":{
#                         "type":"long"
#                     },
#                     "user_location":{
#                         "type":"string"
#                     },
#                     "user_name":{
#                         "type":"string"
#                     },
#                     "user_screen_name":{
#                         "type":"string"
#                     }
#                 }
#             }
#         }
#     })
#
#     return render_to_response('core/es_dashboard.html', {
#     },context_instance=RequestContext(request))


