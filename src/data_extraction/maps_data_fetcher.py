import googlemaps
import requests
import time
import csv
import re
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

maps = googlemaps.Client(API_KEY)

arrondissements = ["1er", "2eme", "3eme", "4eme", "5eme", "6eme",
                   "7eme", "8eme", "9eme", "10eme", "11eme", "12eme", "13eme",
                   "14eme", "15eme", "16eme", "17eme", "18eme", "19eme", "20eme"]
# place_types = ["brasseries"]

def get_places_for_arrondissements(api_key, arrondissements, location="48.8606,2.3376", radius=1000):
    results = []
    
    for district in arrondissements:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': f'Brasserie in Paris {district} arrondissement',
            'location': location,
            'radius': radius,
            'key': api_key,
            'fields': 'name,formatted_address, place_id,rating,user_ratings_total,price_level'  # Requesting necessary fields in the search itself
        }

        while True:
            response = requests.get(url, params=params)
            data = response.json()
            
            # Collect results from this page
            for result in data['results']:
                brasserie_info = {
                    'name': result.get('name'),
                    'address': result.get('formatted_address'),
                    'place_id': result.get('place_id'),
                    'rating': result.get('rating', 'N/A'),
                    'reviews': result.get('user_ratings_total', 'N/A'),
                    'price_level': result.get('price_level', 'N/A'),
                }
                res = get_place_details(result.get('place_id'), api_key)
                website = res if res else 'N/A'
                brasserie_info['website'] = website
                arron = get_district(result.get('formatted_address'))
                brasserie_info['arrondissement'] = arron
                results.append(brasserie_info)
            
            # Handle pagination if there are more results
            next_page_token = data.get('next_page_token')
            if next_page_token and len(results) < 40:
                time.sleep(2)  # Sleep to avoid hitting the API too quickly
                params['pagetoken'] = next_page_token
            else:
                break  # Exit loop if no more results or we have enough results

    return results

def get_place_details(place_id, api_key):
                    # Request details for a specific place
                    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                    params = {
                        'place_id': place_id,
                        'fields': 'website',
                        'key': api_key
                    }
                    
                    response = requests.get(details_url, params=params)
                    data = response.json()                    
                    # Extract the relevant details from the response
                    if 'result' in data:
                        result = data['result']
                        return result.get('website', 'N/A')
                    
def get_district(address):
      x = re.findall('\d{5}', address)[0]
      return x[-2:]

brasseries = get_places_for_arrondissements(API_KEY, arrondissements)

print(len(brasseries))
keys = brasseries[0].keys()

with open('brasseries.csv', 'w', newline='', encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(brasseries)