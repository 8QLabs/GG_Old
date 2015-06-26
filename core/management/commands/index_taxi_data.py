__author__ = 'rajiv'
import json
import csv
from elasticsearch import Elasticsearch
from datetime import datetime

from django.conf import settings

# create instance of elasticsearch
es = Elasticsearch([settings.ELASTIC_SEARCH_HOST])

INDEX_NAME = 'nyc_taxi_data'
TYPE_NAME = 'taxi'

FILENAME = '/mnt/data/taxi/trip_data_1.csv'

def create_taxi_index ():
    print "creating taxi index..."
    es.indices.create(index=INDEX_NAME, body={
        "mappings":{
            "taxi":{
                "properties":{
                    "pickup_datetime":{
                        "type" : "date",
                        "format" : "yyyy-MM-dd HH:mm:ss"
                    },
                    "dropoff_datetime":{
                        "type":"date",
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
                    "distance":{
                        "type" : "float"
                    },
                    "pickup_location": {
                        "type": "geo_point"
                    },
                    "dropoff_location": {
                        "type": "geo_point"
                    },
                    "subtotal_fare": {
                        "type": "float"
                    },
                    "total_fare": {
                        "type": "float"
                    }
                }
            }
        }
    })

def delete_taxi_index():
    print "Deleting taxi index..."
    es.indices.delete(index=INDEX_NAME)


def do_bulk_index(bulk_data):
    # bulk index the data
    print("bulk indexing...")
    res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)

def valid(data):
    if data and data != 0 and data != '':
        return True

    return False

def index_data():
    delete_taxi_index()
    create_taxi_index()

    reader = csv.reader(open(FILENAME,'rU'), delimiter=',', dialect=csv.excel_tab)

    header = reader.next()

    count = 0
    bulk_data = []

    for row in reader:
        if valid(row[5]) and valid(row[6]) and valid(row[7]) and valid(row[8]):
            count = count + 1

            pickup_time = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")

            data_dict = {
                    "pickup_datetime": row[1],
                    "dropoff_datetime": row[2],
                    "year": pickup_time.year,
                    "weekday": pickup_time.weekday(),
                    "hour_of_day": pickup_time.hour,
                    "month_of_year": pickup_time.month,
                    "distance": row[4],
                    "pickup_location": {
                        "lat": row[6],
                        "lon": row[5]
                   },
                    "dropoff_location": {
                        "lat": row[8],
                        "lon": row[7]
                   },
                    "subtotal_fare": row[11],
                    "total_fare": row[16]
            }

            op_dict = {
                "index": {
                    "_index": INDEX_NAME,
                    "_type": TYPE_NAME
                }
            }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)

            if count % 40000 == 0:
                do_bulk_index(bulk_data)
                del bulk_data[:]

    do_bulk_index(bulk_data)
    print count

if __name__ == '__main__':

    index_data()

