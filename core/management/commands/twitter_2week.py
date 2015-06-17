#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
import time
import sys
from datetime import date
import json

auth = tweepy.OAuthHandler('1pHkCAf3Nuj9DSuPM9JYeC9CN', 'mrsLgza7AIiADShBgkYxd5ippzG77ytuiiPnCgGvtY42MD6pq0')
auth.set_access_token('535698855-JDY9iMbTPYQP0yXGYua2pVWS2m1VK2htMuUEyMfO', '27tfGAwjO6uKViTioi6lZbgEFnsI2btV5IsKBGRzYQqkB')
api = tweepy.API(auth)

NYC_CENTER = ['40.7127', '74.0059']
SF_CENTER = ['37.7833', '122.4167']
LA_CENTER = ['34.0500', '118.2500']

city = sys.argv[1]
current_date_str = date.today().strftime("%m-%d-%Y")
FILENAME = '/mnt/data/twitter/historical/' + city + '_' + current_date_str + '.txt'

center_lat = None
center_lon = None
if city == 'ny':
    center_lat = NYC_CENTER[0]
    center_lon = NYC_CENTER[1]
elif city == 'sf':
    center_lat = SF_CENTER[0]
    center_lon = SF_CENTER[1]
elif city == 'la':
    center_lat = LA_CENTER[0]
    center_lon = LA_CENTER[1]

file = open(FILENAME, 'w')

c = tweepy.Cursor(api.search, q='', count='100', geocode=center_lat+','+center_lon+','+'100mi').items()

count = 0
while True:
    try:
        tweet = c.next()
	print json.dumps(tweet._json)
        file.write(json.dumps(tweet._json) + '\n')
        count = count + 1
        # cur.execute(" INSERT INTO NYC_Feb(text, tweet_id, date, user_id, name, followers_count, statuses_count, description, slat, slon, tract, lat, lon) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [  tweet.text.encode('utf8', 'ignore'), tweet.id, tweet.created_at, tweet.author._json['id'], tweet.author._json['name'].encode('utf8', 'ignore'), tweet.author._json['followers_count'], tweet.author._json['statuses_count'], tweet.author._json['description'].encode('utf8', 'ignore'), lat, lon, tract, tweet._json['coordinates']['coordinates'][1], tweet._json['coordinates']['coordinates'][0] ]  )
        # db.commit()
    except tweepy.TweepError:
        time.sleep(60 * 15)
        continue
    except StopIteration:
        break

print count
file.close()


