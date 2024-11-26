from pymongo import MongoClient
import pymongo
import os
import requests

import utils.database
import utils


utils.load_env()


def find_place_from_text(input_text, location=None, radius=2000):
    "Finds a place based on text input and location bias."
    # Retrieve the API key from environment variables
    api_key = os.getenv('GPLACES_API_KEY')

    if not api_key:
        raise ValueError("API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")

    # Define the endpoint URL
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

    # Define the parameters for the request
    params = {
        'fields': 'formatted_address,name,rating,opening_hours,geometry',
        'input': input_text,
        'inputtype': 'textquery',
        'key': api_key
    }
    
    params['locationbias'] = f'circle:{radius}@{location}' if location is not None and radius is not None else None

    # Make the request to the Google Maps API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        response.raise_for_status()  # Raise an exception for HTTP errors
        

def update_geometric_location_pipe(house_properties_collection:pymongo.collection.Collection):
    """ This code will add latitude, longitude data field and update into mongo database. Using google map api to find geometric location
    """
    houses = house_properties_collection.find( {"$and":[{"latitude":{"$exists":False}}, {"longitude":{"$exists":False}}]} )

    for house in houses:
        # get location name each item
        location_name = house.get('location')
        if location_name is None:
            continue
        
        # get geo location by name
        place = find_place_from_text(location_name)
        if len(place['candidates']):
            geo_location = place['candidates'][0]['geometry']['location']
        else:
            continue
        
        house_new = dict(**house, **{
            "latitude":geo_location['lat'],
            "longitude":geo_location['lng']
        })
        
        house_properties_collection.update_one(house, {"$set":house_new}, upsert=False )
        
        
if __name__=="__main__":
    
    mongo = os.environ.get('MONGODB_PASS')
    uri = f"mongodb+srv://dylan:{mongo}@cluster0.wl8mbpy.mongodb.net/"
    client = MongoClient(uri)

    # Connect to the "RetailStore" database
    db = client["real_estate_thai"]

    house_properties_real = db['house_properties_real']
    
    update_geometric_location_pipe(house_properties_real)