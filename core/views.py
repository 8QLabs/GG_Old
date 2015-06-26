from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from elasticsearch import Elasticsearch
from django.http import HttpResponse
from datetime import datetime
from django.db import connections

INDEX_NAME = "tweets"
TYPE_NAME = "tweet"

es = Elasticsearch([settings.ELASTIC_SEARCH_HOST])

def dashboard (request):
    return render_to_response('core/es_dashboard.html', {
    },context_instance=RequestContext(request))

def create_tweet_index ():
    print "Creating Tweet index..."
    es.indices.create(index='tweets', body={
        "mappings":{
            "tweet":{
                "properties":{
                    "date_created":{
                        "type" : "date",
                        "format" : "yyyy-MM-dd HH:mm:ss"
                    },
                    "year": {
                        "type": "integer"
                    },
                    "weekday": {
                        "type": "integer"
                    },
                    "hour_of_day": {
                        "type": "integer"
                    },
                    "month_of_year": {
                        "type": "integer"
                    },
                    "followers_count":{
                        "type":"long"
                    },
                    # "friends_count":{
                    #     "type":"long"
                    # },
                    "statuses_count":{
                        "type":"long"
                    },
                    "location": {
                        "type": "geo_point"
                    },
                    "text":{
                        "type":"string"
                    },
                    # "timestamp_ms":{
                    #     "type":"long"
                    # },
                    # "user_agent":{
                    #     "type":"string"
                    # },
                    "user_id":{
                        "type":"long"
                    },
                    # "user_location":{
                    #     "type":"string"
                    # },
                    "user_name":{
                        "type":"string"
                    }
                    # "user_screen_name":{
                    #     "type":"string"
                    # }
                }
            }
        }
    })

def delete_tweet_index():
    print "Deleting tweet index..."
    es.indices.delete(index=INDEX_NAME)

def do_bulk_index(bulk_data):
    # bulk index the data
    print("bulk indexing...")
    res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)

def index_janfeb_tweets (request):
    # delete_tweet_index()
    # create_tweet_index()

    cursor = connections['twitter'].cursor()

    offset = 1
    bulk_data = []
    limit = 5000
    cursor.execute("select * from NYC_Jan order by id limit 1, " + str(limit))
    rows = cursor.fetchall()

    while rows:
        print "Offset is currently " + str(offset)
        for row in rows:
            # pickup_time = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")

            date_created = row[3]

            date_created_str = date_created.strftime('%Y-%m-%d %H:%M:%S')

            data_dict = {
                "date_created": date_created_str,
                "year": date_created.year,
                "weekday": date_created.weekday(),
                "hour_of_day": date_created.hour,
                "month_of_year": date_created.month,
                "user_id": row[4],
                "user_name": row[5],
                "followers_count": row[6],
                "statuses_count": row[7],
                "location": {
                    "lat": row[9],
                    "lon": row[10]
                },
                "text": row[1]
            }

            op_dict = {
                "index": {
                    "_index": INDEX_NAME,
                    "_type": TYPE_NAME,
                    "_id": row[2]
                }
            }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)

        do_bulk_index(bulk_data)
        del bulk_data[:]

        offset = offset + limit
        cursor.execute("select * from NYC_Jan order by id limit " + str(offset) + ", " + str(limit))
        rows = cursor.fetchall()

    return HttpResponse(1)




