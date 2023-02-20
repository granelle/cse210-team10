from django.shortcuts import render
from django.http import HttpResponse
#import googlemaps
#import requests

# Create your views here.
# request -> response
# request handler
# action
# django calls this a "view"

# Mohana and Ye connected homepage to backend 2/20/23
def say_hello(request):
    # pull data from db
    # send email, etc
    #return HttpResponse('Mohana says Hello world')
    #return render(request, 'hello.html',{'name':'Ye'})
    return render(request, 'home.html')

# Junyi backend work
# Create your views here.
def search_restaurant_near_home(request, home_address):
    gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
    geocode_result = gmaps.geocode(home_address)
    lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=1000&type=restaurant&keyword=restaurant&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_restaurants = len(response.json()['results'])
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_restaurants
    return (number_of_restaurants, avg_rating)
    #Todo: return to rendering a result page and show current return data in that page.

def search_hospital_near_home(request, home_address):
    gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
    geocode_result = gmaps.geocode(home_address)
    lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=1000&type=hospital&keyword=hospital&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_hospitals = len(response.json()['results'])
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_hospitals
    return (number_of_hospitals, avg_rating)
    #Todo: return to rendering a result page and show current return data in that page.

def search_grocery_store_near_home(request, home_address):
    gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
    geocode_result = gmaps.geocode(home_address)
    lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=1000&type=supermarket&keyword=supermarket&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_stores = len(response.json()['results'])
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_stores
    return (number_of_stores, avg_rating)
    #Todo: return to rendering a result page and show current return data in that page.

# def time_commuting_from_home_to_target(request, home_address, target_address):


    