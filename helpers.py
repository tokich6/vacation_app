from os import environ
import requests

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


