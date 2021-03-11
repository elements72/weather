from time import sleep
from albert import *
from geopy import geocoders, Nominatim
import requests
import json
"""
Shows the weather for the selected city.

The extension shows the main informations about the wheater of the selected city today.

Synopsis: <trigger> [city]
"""
__doc__     = "Show the weather of the selected city"
__title__   = "weather"
__version__ = "0.1.0"
__triggers__ = "wt "
__authors__  = "elements72, adrianoRieti"
__py_deps__ = "geopy"

informations={}

def initialize():
    global informations
    f = open("data.json", "r")
    informations = json.load(f)
    f.close()

def handleQuery(query):
    if not query.isTriggered:
        return
    city = query.string
    data = getData(city, query)
    if query.isValid:
        return make_item(data)


def getData(city, query):
    data = None
    sleep(1)
    if query.isValid:
        geocoder = Nominatim(user_agent="albert-weather")
        location = geocoder.geocode(city, featuretype="city", language="en")
        info(str(location))
        if location != None:
            url = "http://www.7timer.info/bin/api.pl?lon={0}&lat={1}&lang=it&product=civillight&output=json".format(location.longitude, location.latitude)
            response = requests.get(url)
            data = json.loads(response.text)
            data = {"wtInfo": data["dataseries"][0], "city": location.address}
    return data


def make_item(data):
    text = "City not found"
    temperature = ""
    imgDir = "./images/"
    iconPath = imgDir + "warning.png"
    if data != None:
        wtInfo = data["wtInfo"]
        text = data["city"]
        iconPath = imgDir + informations[wtInfo["weather"]]["iconPath"]
        temperature = informations[wtInfo["weather"]]["description"] + ", Max:{}° Min:{}°".format(wtInfo["temp2m"]["max"], wtInfo["temp2m"]["min"])
    return [Item(
        id = __title__,
        text = text,
        subtext = temperature,
        icon = iconPath,
        actions = [],
    )]  