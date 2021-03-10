from datetime import date
from time import sleep
from albert import *
from geopy import *
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
    if data != None:
        return make_item(city, data)
    else:
        return
        #return make_item("City not found", None)

def getData(city, query):
    if query.isValid:
        geocoder = Nominatim(user_agent="http")
        location = geocoder.geocode(city)
        if location != None:
            url = "http://www.7timer.info/bin/api.pl?lon={0}&lat={1}&lang=it&product=civillight&output=json".format(location.longitude, location.latitude)
            response = requests.get(url)
            data = json.loads(response.text)
            return data["dataseries"][0]
    return None


def make_item(city, data):
    text = city
    temperature = ""
    imgDir = "./images/"
    iconPath = imgDir + "warning.png"
    if data != None:
        iconPath = imgDir + informations[data["weather"]]["iconPath"]
        text = text + " " + informations[data["weather"]]["description"]
        temperature = "Max:{}° Min:{}°".format(data["temp2m"]["max"], data["temp2m"]["min"])
    return [Item(
        id = __title__,
        text = text,
        subtext = temperature,
        icon = iconPath,
        actions = [],
    )]  