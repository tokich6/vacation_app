from os import environ
import requests
from flask import redirect, render_template, request, session, url_for
from functools import wraps
from datetime import date


API_KEY = environ.get('API_KEY')

# find the id of the typed in location/destination
def search_location_id(location):
    # Contact API
    try:
        url = "https://hotels4.p.rapidapi.com/locations/search"
        querystring = {"query":{location}}
        headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.RequestException:
        return None      
    # Parse response
    try:
        result = response.json()
        destinationID = result['suggestions'][0]['entities'][0]['destinationId']
        return destinationID
    except (KeyError, TypeError, ValueError):
        return None    

def list_properties(id, check_in, check_out, adults1):
    # contact api and find available properties as per search parameteres
    try:
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"currency":"USD","locale":"en_US","sortOrder":"GUEST_RATING",
        "destinationId":{id},"pageNumber":"1","checkIn":{check_in},"checkOut":{check_out},"pageSize":"25","adults1":{adults1}}
        headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.RequestException:
        return None     
     # Parse response
    try:
        result = response.json()
        return {
            'header': result['data']['body']['header'],
            'totalCount':  result['data']['body']['searchResults']['totalCount'],
            'hotels': result['data']['body']['searchResults']['results']
        }
    except (KeyError, TypeError, ValueError):
        return None    

def get_hotel_details(id, check_in, check_out, adults1):
    # contact api to get individual hotel details
    try:
        url = "https://hotels4.p.rapidapi.com/properties/get-details"
        querystring = {"locale":"en_US","currency":"USD","checkOut":{check_out},"adults1":{adults1},"checkIn":{check_in},"id":{id}}
        headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.RequestException:
        return None     
     # Parse response
    try:
        result = response.json()
        return {
            'amenities': result['data']['body']['overview']['overviewSections'][0]['content'],
            'what_is_around': result['data']['body']['overview']['overviewSections'][1]['content'],
            'property_description': result['data']['body']['propertyDescription'],
            'first_room': result['data']['body']['roomsAndRates']['rooms'][0]
        }
    except (KeyError, TypeError, ValueError):
        return None    

def get_hotel_photos(id):
    # contact api to get individual hotel details
    try:
        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        querystring = {"id":{id}}
        headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
    except requests.RequestException:
        return None     

     # Parse response
    try:
        result = response.json()
        return {
            'hotel_images': result['hotelImages'],
            'room_images': result['roomImages']
        }
    except (KeyError, TypeError, ValueError):
        return None    

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def str_to_date(string):
  [year, month, day] = map(int, string.split('-'))
  return date(year, month, day)

def get_days(start, end):
  return (str_to_date(end) - str_to_date(start)).days

def str_to_bool(string):
    d = {'True': True, 'False': False}
    return d.get(string, string)

# to be used for cancel_before date - the API returns different formats (incl time, letters attached to date)
def reduce_str_len(str):
    str = str[0:10]
    return str