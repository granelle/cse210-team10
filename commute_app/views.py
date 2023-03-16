import time
from django.shortcuts import render
from django.http import HttpResponse
import googlemaps
import requests
from math import *
from .models import Search
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
import re

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
from commute_app import models


def go_home(request):
    # Go to home page.
    return render(request, 'home.html')

# Se-eun 2/22/23
def display_scores(request):
    print(request.user.username)
    # display scores
    if request.method == 'POST':
        if request.POST['search_method'] == "search":
            inputContent = {
                'start_name' : request.POST['start_name'],
                'start_addr': request.POST['start_addr'],
                'target_name': request.POST['target_name'],
                'target_addr': request.POST['target_addr'],
                'commute_weight': request.POST['commute_weight'],
                'restaurant_weight': request.POST['restaurant_weight'],
                'grocery_weight': request.POST['grocery_weight'],
                'medical_weight': request.POST['medical_weight'],
                'mode_list': request.POST.getlist('trans-modes')
            }
            return scores_generator(request, userInput=inputContent)
        else:
            print(request.POST['start_addr'])
            inputContent = {
                'restaurant_info': request.POST['restaurant_info'],
                'hospital_info': request.POST['hospital_info'],
                'grocery_info': request.POST['grocery_info'],
                'driving_info': request.POST[ 'driving_info'],
                'overall_info': request.POST['overall_info'],
                'commuting_info': request.POST['commuting_info'],
                'home_address': request.POST['start_addr'], # change home_address here later, inconsistent naming
                'target_address': request.POST['target_addr'],
                'start_nickname': request.POST['start_name'],
                'target_nickname': request.POST['target_name'],
                'is_favorite': request.POST['is_favorite'],
            }
            # time.sleep(5)
            add_favorite_entry_to_database(inputContent)
            return render(request, 'rating.html', context = inputContent)
    else:
        # TODO: some error check
        return render(request, 'error.html')

# Se-eun 2/22/23
def display_scores(request):
    print(request.user.username)
    # Display scores for the score page.
    if request.method == 'POST':
        if request.POST['search_method'] == "search":
            inputContent = {
                'start_name' : request.POST['start_name'],
                'start_addr': request.POST['start_addr'],
                'target_name': request.POST['target_name'],
                'target_addr': request.POST['target_addr'],
                'commute_weight': request.POST['commute_weight'],
                'restaurant_weight': request.POST['restaurant_weight'],
                'grocery_weight': request.POST['grocery_weight'],
                'medical_weight': request.POST['medical_weight'],
                'mode_list': request.POST.getlist('trans-modes')
            }
            return scores_generator(request, userInput=inputContent)
        else:
            print(request.POST['start_addr'])
            inputContent = {
                'restaurant_info': request.POST['restaurant_info'],
                'hospital_info': request.POST['hospital_info'],
                'grocery_info': request.POST['grocery_info'],
                'driving_info': request.POST[ 'driving_info'],
                'overall_info': request.POST['overall_info'],
                'commuting_info': request.POST['commuting_info'],
                'home_address': request.POST['start_addr'], # change home_address here later, inconsistent naming
                'target_address': request.POST['target_addr'],
                'start_nickname': request.POST['start_name'],
                'target_nickname': request.POST['target_name'],
            }
            add_favorite_entry_to_database(request, inputContent)
            return render(request, 'rating.html', context = inputContent)

def add_favorite_entry_to_database(request, input):
    # Add favorite entry to database.
    if(request.user.is_authenticated):
        tmp = Search.objects.filter(startAdd =  input['home_address'], targetAdd=input['target_address'], username=request.user.username)
        if len(tmp) != 0:
            return
        s1 = Search.objects.create(username = request.user.username, startAdd = input['home_address'], startNick = input['start_nickname'], 
        targetAdd = input['target_address'], targetNick = input['target_nickname'], 
        overallScore = input['overall_info'], driveScore = input['driving_info'], restScore = input['restaurant_info'], hospScore = input['hospital_info'],
        groceryScore = input['grocery_info'])
    return


def scores_generator(request, userInput):
    # Generate scores for given start and target address.
    return search_near_home(request, weights_list= [userInput['commute_weight'], userInput['restaurant_weight'], userInput['grocery_weight'], userInput['medical_weight']], 
    start_address = userInput['start_addr'], 
    target_address = userInput['target_addr'], start_nickname = userInput['start_name'], target_nickname = userInput['target_name'], mode_list = userInput['mode_list'])

# Xinyu 2/22/23
def display_tutorial(request):
    # display tutorial page.
    return render(request, 'tutorial.html')

# Se-eun 3/10/23
def display_contact(request):
    # display contact page.
    return render(request, 'contact.html')

def display_error(request):
    # display error page.
    return render(request, 'error.html')

def display_test(request):
    # display error page.
    return render(request, 'test.html')

def display_favorite(request):
    # Display favorite page.
    search_list = Search.objects.filter(username=request.user.username).order_by('-overallScore')
    mydict = {
        'search_list':search_list
    }
    return render(request, 'favorite.html', context = mydict)

class display_signup(generic.CreateView):
    # Display signup page.
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# Junyi backend work
# Create your views here.
def search_restaurant_near_home(gmaps, home_address):
    # Search restaurants near home.
    geocode_result = gmaps.geocode(home_address)
    try:
        lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    except IndexError as e:
        raise e
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=5000&type=restaurant&keyword=restaurant&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_restaurants = len(response.json()['results'])
    if number_of_restaurants == 0:
        return (0, 0)
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_restaurants
    return (number_of_restaurants, avg_rating)

def search_hospital_near_home(gmaps, home_address):
    # Search hosppitals near home.
    geocode_result = gmaps.geocode(home_address)
    try:
        lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    except IndexError as e:
        raise e
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=3000&type=hospital&keyword=hospital&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_hospitals = len(response.json()['results'])
    if number_of_hospitals == 0:
        return (0, 0)
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_hospitals
    return (number_of_hospitals, avg_rating)

def search_grocery_store_near_home(gmaps, home_address):
    # Search grocery stores near home.
    geocode_result = gmaps.geocode(home_address)
    try:
        lat, lng = str(geocode_result[0]['geometry']['location']['lat']), str(geocode_result[0]['geometry']['location']['lng'])
    except IndexError as e:
        raise e
    #compose the url
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat +"%2C" + lng + "&radius=1000&type=supermarket&keyword=supermarket&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc"
    response = requests.request("GET", url, headers = {}, data = {})
    number_of_stores = len(response.json()['results'])
    if number_of_stores == 0:
        return (0, 0)
    avg_rating = sum(e['rating'] for e in response.json()['results']) / number_of_stores
    return (number_of_stores, avg_rating)

def search_near_home(request, weights_list, start_address, target_address, start_nickname, target_nickname, mode_list=['driving', 'walking', 'bicycling', 'transit']):
    # Commute score for score near home.
    
    # Use default addresses if user input address is empty.
    if (start_address == ''):
        start_address= '3869 Miramar St, La Jolla, CA'
    if (target_address == ''):
        target_address = '9500 Gilman Dr, La Jolla, CA'

    # If nickname is not specified, send address instead.
    if (start_nickname == ''):
        start_nickname = start_address

    if (target_nickname == ''):
        target_nickname = target_address
    
    gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
    try:
        restaurant_info = score_nearby_restaurants(gmaps, start_address)
        hospital_info = score_nearby_hospitals(gmaps, start_address)
        grocery_info = score_nearby_stores(gmaps, start_address)
        driving_info = score_commuting(gmaps, start_address, target_address, mode="driving")
    except IndexError as e:
        return render(request, 'error.html')
    overall_info = min(5, round((driving_info * int(weights_list[0]) + restaurant_info * int(weights_list[1]) + grocery_info * int(weights_list[2]) + hospital_info * int(weights_list[3]))/sum(int(i) for i in weights_list), 2))
    commuting_info = {}
    for mode in mode_list:
        try:
            commuting_info[mode] = score_commuting(gmaps, start_address, target_address, mode)
        except IndexError as e:
            return render(request, 'error.html')

    context = {
        'restaurant_info': restaurant_info,
        'hospital_info': hospital_info,
        'grocery_info': grocery_info,
        'driving_info': driving_info,
        'overall_info': overall_info,
        'commuting_info': commuting_info,
        'home_address': start_address, # change home_address here later, inconsistent naming
        'target_address': target_address,
        'start_nickname': start_nickname,
        'target_nickname': target_nickname
    }

    return render(request, 'rating.html', context = context)

def find_address_pair_in_database(request, start_addr, target_addr):
    # check if target address & start address exist in the database
    is_favorite = "unfav" 
    
    search_list = Search.objects.filter(username=request.user.username, startAdd = start_addr, targetAdd = target_addr)
    if(search_list != ''):
        is_favorite = "fav"

def time_commuting_from_home_to_target(gmaps, source_address, target_address, mode):
    # Commute time from home to target.
    s_geocode_result = gmaps.geocode(source_address)
    t_geocode_result = gmaps.geocode(target_address)
    try:
        s_lat, s_lng, t_lat, t_lng = str(s_geocode_result[0]['geometry']['location']['lat']), str(s_geocode_result[0]['geometry']['location']['lng']), str(t_geocode_result[0]['geometry']['location']['lat']), str(t_geocode_result[0]['geometry']['location']['lng'])
    except IndexError as e:
        raise e
    
    result_list = []
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + s_lat + "%2C" + s_lng + "&destinations=" + t_lat + "%2C" + t_lng + "&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc&mode=" + mode 
    response = requests.request("GET", url, headers = {}, data = {})
    est_time = response.json()['rows'][0]['elements'][0]['duration']['text']
    distance = response.json()['rows'][0]['elements'][0]['distance']['text']
    return (est_time, distance)

def score_nearby_restaurants(gmaps, home_address):
    # Commute score for nearby restaurants.
    try:
        num_of_restaurants, avg_rating = search_restaurant_near_home(gmaps, home_address)
    except IndexError as e:
        raise e
    score = log(0.1 * num_of_restaurants + 0.1) + avg_rating
    return min(5, round(score, 2))

def score_nearby_hospitals(gmaps, home_address):
    # Commute score for nearby hospitals.
    try:
        num_of_hospitals, avg_rating = search_hospital_near_home(gmaps, home_address)
    except IndexError as e:
        raise e
    score = log(0.1 * num_of_hospitals + 0.1) + avg_rating
    return min(5, round(score, 2))

def score_nearby_stores(gmaps, home_address):
    # Commute score for nearby stores.
    try:
        num_of_stores, avg_rating = search_grocery_store_near_home(gmaps, home_address)
    except IndexError as e:
        raise e
    score = log(0.1 * num_of_stores + 0.1) + avg_rating
    return min(5, round(score, 2))

def score_commuting(gmaps, home_address, targe_address, mode):
    # Commute score for commuting time.
    try:
        est_time, _ = time_commuting_from_home_to_target(gmaps, home_address, targe_address, mode)
    except IndexError as e:
        raise e
    time_list = re.findall(r'\d+', est_time)
    if len(time_list) == 1:
        time_in_minute = int(time_list[0])
    elif len(time_list) == 2:
        time_in_minute = int(time_list[0]) * 60 + int(time_list[1])
    elif len(time_list) == 3:
        time_in_minute = int(time_list[0]) * 60 * 24 + int(time_list[1]) * 60 + int(time_list[2])
    if time_in_minute < 15:
        return 5
    else:
        return min(5, round(75 / time_in_minute, 2))
