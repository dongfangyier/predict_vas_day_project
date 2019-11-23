import pandas as pd
import requests
from requests.exceptions import ReadTimeout, ConnectTimeout
from math import radians, sin, cos, asin, sqrt


def addr_to_cod(geo):
    '''
    a test function of converted address to longitude and latitude
    :param geo:
    :return:
    '''
    parameters = {'address': geo, 'key': '001d58dcca24742dcc00f9bad812309d'}
    base = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    loc = 0
    try:
        response = requests.get(base, parameters, timeout=2)
        if response.status_code == 200:
            answer = response.json()
            loc = answer['geocodes'][0]['location']
        else:
            pass
    except (ReadTimeout, ConnectTimeout):
        pass
    return loc
# print(addr_to_cod('北京市北京市丰台区丰台区南苑西居住区'))


# here not used
def _calaulate_distance(origins, destination):
    '''
    calculate linear distance from longitude and latitude
    :param origins:
    :param destination:
    :return:
    '''
    parameters = {'origins': origins, 'destination': destination, 'key': '001d58dcca24742dcc00f9bad812309d', 'type': 0}
    base = 'https://restapi.amap.com/v3/distance?parameters'
    distance = None
    try:
        response = requests.get(base, parameters, timeout=2)
        if response.status_code == 200:
            answer = response.json()
            distance = answer['results'][0]['distance']
        else:
            pass
    except (ReadTimeout, ConnectTimeout, Exception):
        pass
    return distance
# print(calaulate_distance('116.358105,39.961555', '116.186857,39.936762'))


def get_place(long_lat):
    '''
    get place by the longitude and latitude
    :param long_lat:longitude and latitude
    :return:the name of the place
    '''
    parameters = {'location': long_lat, 'key': '001d58dcca24742dcc00f9bad812309d', 'poitype': '商务写字楼', 'radius': 1000,
                  'extensions': 'all', 'batch': False, 'roadlevel': 0}
    base = 'https://restapi.amap.com/v3/geocode/regeo?parameters'
    place = None
    try:
        response = requests.get(base, parameters, timeout=2)
        if response.status_code == 200:
            answer = response.json()
            place = answer['regeocode']['formatted_address']
        else:
            pass
    except (ReadTimeout, ConnectTimeout, Exception):
        pass
    return place
# print(get_place('116.358105,39.966790'))


def geodistance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000
    return dis


def calaulate_distance(origins, destination):
    '''
    calculate linear distance from longitude and latitude
    :param origins:
    :param destination:
    :return:
    '''
    temp = str(origins).split(',')
    lng1 = float(temp[0])
    lat1 = float(temp[1])
    temp = str(destination).split(',')
    lng2 = float(temp[0])
    lat2 = float(temp[1])

    return geodistance(lng1, lat1, lng2, lat2)
# print(calaulate_distance('116.369047,39.805213', '116.364287,39.798569'))
