import pandas as pd 
import requests
import json
import random
import math
import urllib.parse

from math import sin, cos, sqrt, atan2, radians

shops = pd.read_csv('BBTLocation_new.csv')

def getLatLon(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + api_key
    print('Requesting: ', url)
    try:
        response_content = json.loads(requests.get(url).content)
    except:
        response_content = None
        
    if response_content:
        lat = response_content['results'][0]['geometry']['location']['lat']
        lon = response_content['results'][0]['geometry']['location']['lng']
        return [lat, lon]
    
    else:
        return [None, None]

def extractLatLon(df):
    df['lat'] = df['LatLon'].apply(lambda x: x[0])
    df['lon'] = df['LatLon'].apply(lambda x: x[1])
    df['Address'] = df['Address'].apply(lambda x: x.replace('\n', ''))
    df = df.drop(['LatLon', 'Address_temp'], axis=1)
    return df

shops

shops['Address_temp'] = shops[['Brand', 'Address']].agg(', '.join, axis=1)
#shops['Address_temp'] = shops['Address_temp'].apply(lambda x: x.replace('\n', ' '))
shops['Address_temp'] = shops['Address_temp'].apply(lambda x: urllib.parse.quote(x))

api_key = 'AIzaSyCd2hX-Tuw1RjNzVy3EylUPb9_qIWL_T70'

shops['LatLon'] = shops['Address_temp'].apply(lambda x: getLatLon(x))

shops = extractLatLon(shops)

shops

shops.to_csv('BBTLocation(Geocoded).csv', index=False)