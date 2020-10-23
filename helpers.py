# from os import environ
from os import environ
import requests
from flask import redirect, render_template, request, session, url_for
from functools import wraps
from amadeus import Client, ResponseError, Location


# initialize Amadeus client - export AMADEUS_CLIENT_ID && AMADEUS_CLIENT_SECRET environment variables required
amadeus = Client()

# city_code, check_in, check_out, adults1
def list_hotels_by_city(city_code, check_in, check_out, adults1, rooms):
    try:
        # Get list of Hotels by city code
        response = amadeus.shopping.hotel_offers.get(cityCode=city_code,checkInDate=check_in,checkOutDate=check_out,adults=adults1,
         roomQuantity=rooms,currency='USD')
    except ResponseError as error:
        raise error
    # Parse response
    try:
        result = response.data
        print(result)
        return {
            'hotels': result
        }
    except (KeyError, TypeError, ValueError):
        return None    

# Airport and City Search (autocomplete)
# Find all the cities and airports starting by 'LON' 
def get_locations():
    try:
        response = amadeus.reference_data.locations.get(keyword='LON', subType=Location.ANY)
    except ResponseError as error:
        raise error
    # Parse response
    try:
        result = response.data
        print(result)
        return result
    except (KeyError, TypeError, ValueError):
        return None        

# Travel Recommendations
amadeus.reference_data.recommended_locations.get(cityCodes='PAR', travelerCountryCode='FR')



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# find the id of the typed in location/destination
# def search_location_id(location):
#     # Contact API
#     try:
#         url = "https://hotels4.p.rapidapi.com/locations/search"
#         querystring = {"query":{location}}
#         headers = {
#         'x-rapidapi-host': "hotels4.p.rapidapi.com",
#         'x-rapidapi-key': API_KEY
#         }
#         response = requests.request("GET", url, headers=headers, params=querystring)
#     except requests.RequestException:
#         return None    
    
#     # Parse response
#     try:
#         result = response.json()
#         # print(result)
#         destinationID = result['suggestions'][0]['entities'][0]['destinationId']
#         return destinationID
#     except (KeyError, TypeError, ValueError):
#         return None    

# def list_properties(id, check_in, check_out, adults1):
#     # contact api and find available properties as per search parameteres
#     try:
#         url = "https://hotels4.p.rapidapi.com/properties/list"
#         querystring = {"currency":"USD","locale":"en_US","sortOrder":"GUEST_RATING",
#         "destinationId":{id},"pageNumber":"1","checkIn":{check_in},"checkOut":{check_out},"pageSize":"25","adults1":{adults1}}
#         headers = {
#         'x-rapidapi-host': "hotels4.p.rapidapi.com",
#         'x-rapidapi-key': API_KEY
#         }
#         response = requests.request("GET", url, headers=headers, params=querystring)
#     except requests.RequestException:
#         return None     

#      # Parse response
#     try:
#         result = response.json()
#         return {
#             'header': result['data']['body']['header'],
#             'totalCount':  result['data']['body']['searchResults']['totalCount'],
#             'hotels': result['data']['body']['searchResults']['results']
#         }
#     except (KeyError, TypeError, ValueError):
#         return None    

# def get_hotel_details(id, check_in, check_out, adults1):
#     # contact api to get individual hotel details
#     try:
#         url = "https://hotels4.p.rapidapi.com/properties/get-details"
#         querystring = {"locale":"en_US","currency":"USD","checkOut":{check_out},"adults1":{adults1},"checkIn":{check_in},"id":{id}}
#         headers = {
#         'x-rapidapi-host': "hotels4.p.rapidapi.com",
#         'x-rapidapi-key': API_KEY
#         }
#         response = requests.request("GET", url, headers=headers, params=querystring)
#     except requests.RequestException:
#         return None     

#      # Parse response
#     try:
#         result = response.json()
#         return {
#             'amenities': result['data']['body']['overview']['overviewSections'][0]['content'],
#             'what_is_around': result['data']['body']['overview']['overviewSections'][1]['content'],
#             'property_description': result['data']['body']['propertyDescription']
#             # 'totalCount':  result['data']['body']['searchResults']['totalCount'],
#             # 'hotels': result['data']['body']['searchResults']['results']
#         }
#     except (KeyError, TypeError, ValueError):
#         return None    

# def get_hotel_photos(id):
    # contact api to get individual hotel details
    # try:
    #     url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    #     querystring = {"id":{id}}
    #     headers = {
    #     'x-rapidapi-host': "hotels4.p.rapidapi.com",
    #     'x-rapidapi-key': API_KEY
    #     }
    #     response = requests.request("GET", url, headers=headers, params=querystring)
    # except requests.RequestException:
    #     return None     

    #  # Parse response
    # try:
    #     result = response.json()
    #     return {
    #         'hotel_images': result['hotelImages'],
    #         'room_images': result['roomImages']
    #     }
    # except (KeyError, TypeError, ValueError):
    #     return None    


