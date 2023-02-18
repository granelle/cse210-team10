from django.shortcuts import render
import googlemaps
import requests

# Create your views here.
def search_restaurant_near_home(request, home_address):
    gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
    geocode_result = gmaps.geocode(home_address)
    lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=1000&type=restaurant&keyword=cruise&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_restaurants = len(response.json()['results'])
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_restaurants
    return (number_of_restaurants, avg_rating)
