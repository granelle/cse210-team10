from django.shortcuts import render
from django.http import HttpResponse
import googlemaps
import requests
from math import *
from .models import Search

# Create your views here.
# request -> response
# request handler
# action
# django calls this a "view"

# Mohana database stuff
def database_test(request):
    Search.objects.create(startAdd = "4067 Miramar st.", startNick = "Mo grad housing", targetAdd = "39 Santa Catalina Aisle", targetNick = "Irvine home")
    return HttpResponse("Hi Mohana")


# Mohana and Ye connected homepage to backend 2/20/23
def go_home(request):
    # pull data from db
    # send email, etc
    #return HttpResponse('Mohana says Hello world')
    #return render(request, 'hello.html',{'name':'Ye'})
    return render(request, 'home.html')

# Se-eun 2/22/23
def display_scores(request):
    # display scores
    # TODO: "go" button at home should direct to this page
    # TODO: solve the incorrect address input -> jump to error page
    return render(request, 'scores.html')
    # if request.method == 'POST':
    #     inputContent = {
    #         'start_name' : request.POST['start_name'],
    #         'start_addr': request.POST['start_addr'],
    #         'target_name': request.POST['target_name'],
    #         'target_addr': request.POST['target_addr'],
    #         'commute_weight': request.POST['commute_weight'],
    #         'restaurant_weight': request.POST['restaurant_weight'],
    #         'grocery_weight': request.POST['grocery_weight'],
    #         'medical_weight': request.POST['medical_weight']
    #     }
    #     return scores_generator(request, userInput = inputContent)
    # else:
    #     # TODO: some error check
    #     return render(request, 'error.html')

def scores_generator(request, userInput):
    # TODO: figure out the algorithm to generate score
    # It's a basic scores calculate with only commute
    return search_near_home(request, home_address = userInput['start_addr'], target_address = userInput['target_addr'])


# Xinyu 2/22/23
def display_tutorial(request):
    # display tutorial
    # TODO: "about" button at home should direct to this page
    # TODO: "get start" at this page should direct to home page
    return render(request, 'tutorial.html')

def display_error(request):
    # display error
    # TODO: "go" button at home should direct to this page when errors occur
    # TODO: "go back" button at this page should direct to home page 
    return render(request, 'error.html')

def display_test(request):
    # display error
    # TODO: "go" button at home should direct to this page when errors occur
    # TODO: "go back" button at this page should direct to home page 
    return render(request, 'test.html')

# Junyi backend work
# Create your views here.
def search_restaurant_near_home(gmaps, home_address):
    geocode_result = gmaps.geocode(home_address)
    lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=5000&type=restaurant&keyword=restaurant&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_restaurants = len(response.json()['results'])
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_restaurants
    return (number_of_restaurants, avg_rating)
    #Todo: return to rendering a result page and show current return data in that page.

def search_hospital_near_home(gmaps, home_address):
    geocode_result = gmaps.geocode(home_address)
    lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=3000&type=hospital&keyword=hospital&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_hospitals = len(response.json()['results'])
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_hospitals
    return (number_of_hospitals, avg_rating)
    #Todo: return to rendering a result page and show current return data in that page.

def search_grocery_store_near_home(gmaps, home_address):
    geocode_result = gmaps.geocode(home_address)
    lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=1000&type=supermarket&keyword=supermarket&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_stores = len(response.json()['results'])
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_stores
    return (number_of_stores, avg_rating)
    #Todo: return to rendering a result page and show current return data in that page.

def search_near_home(request, home_address='3869 Miramar St, La Jolla, CA', target_address = '9500 Gilman Dr, La Jolla, CA'):
    gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
    restaurant_info = score_nearby_restaurants(gmaps, home_address)
    hospital_info = score_nearby_hospitals(gmaps, home_address)
    grocery_info = score_nearby_stores(gmaps, home_address)
    commuting_info = time_commuting_from_home_to_target(gmaps, home_address, target_address)
    context = {
        'restaurant_info': restaurant_info,
        'hospital_info': hospital_info,
        'grocery_info': grocery_info,
        'commuting_info': commuting_info
    }
    return render(request, 'scores.html', context = context)


def time_commuting_from_home_to_target(gmaps, source_address, target_address):
    s_geocode_result = gmaps.geocode(source_address)
    t_geocode_result = gmaps.geocode(target_address)
    s_lat, s_lng, t_lat, t_lng = str(s_geocode_result[0]['geometry']['location']['lat']), str(s_geocode_result[0]['geometry']['location']['lng']), str(t_geocode_result[0]['geometry']['location']['lat']), str(t_geocode_result[0]['geometry']['location']['lng'])
    # "https://maps.googleapis.com/maps/api/distancematrix/json?origins=40.6655101%2C-73.89188969999998&destinations=40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key=YOUR_API_KEY"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + s_lat + "%2C" + s_lng + "&destinations=" + t_lat + "%2C" + t_lng + "&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    est_time = response.json()['rows'][0]['elements'][0]['duration']['text']
    distance = response.json()['rows'][0]['elements'][0]['distance']['text']
    return (est_time, distance)

def score_nearby_restaurants(gmaps, home_address):
    num_of_restaurants, avg_rating = search_restaurant_near_home(gmaps, home_address)
    score = log(0.1 * num_of_restaurants + 0.1) + avg_rating
    return score

def score_nearby_hospitals(gmaps, home_address):
    num_of_hospitals, avg_rating = search_hospital_near_home(gmaps, home_address)
    score = log(0.1 * num_of_hospitals + 0.1) + avg_rating
    return score

def score_nearby_stores(gmaps, home_address):
    num_of_stores, avg_rating = search_grocery_store_near_home(gmaps, home_address)
    score = log(0.1 * num_of_stores + 0.1) + avg_rating
    return score

