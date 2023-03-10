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
    # pull data from db
    # send email, etc
    #return HttpResponse('Mohana says Hello world')
    #return render(request, 'hello.html',{'name':'Ye'})
    return render(request, 'home.html')

# Se-eun 2/22/23
def display_scores(request):
    print(request.user.username)
    # display scores
    # TODO: "go" button at home should direct to this page
    # TODO: solve the incorrect address input -> jump to error page
    #return render(request, 'rating.html')
    if request.method == 'POST':
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
        return scores_generator(request, userInput = inputContent)
    else:
        # TODO: some error check
        return render(request, 'error.html')

def scores_generator(request, userInput):
    # TODO: figure out the algorithm to generate score
    # It's a basic scores calculate with only commute
    #return search_near_home(request, home_address = userInput['start_addr'], 
    #target_address = userInput['target_addr'], start_nickname = userInput['start_name'], target_nickname= userInput['target_name'])
    return search_near_home(request, weights_list= [userInput['commute_weight'], userInput['restaurant_weight'], userInput['grocery_weight'], userInput['medical_weight']], 
    start_address = userInput['start_addr'], 
    target_address = userInput['target_addr'], start_nickname = userInput['start_name'], target_nickname = userInput['target_name'], mode_list = userInput['mode_list'])

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

def display_favorite(request):
    search_list = Search.objects.filter(username=request.user.username)
    #search_list = models.Search.objects.all()
    mydict = {
        'search_list':search_list
    }
    return render(request, 'favorite.html', context = mydict)

class display_signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# Junyi backend work
# Create your views here.
def search_restaurant_near_home(gmaps, home_address):
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
    #Todo: return to rendering a result page and show current return data in that page.

def search_hospital_near_home(gmaps, home_address):
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
    #Todo: return to rendering a result page and show current return data in that page.

def search_grocery_store_near_home(gmaps, home_address):
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
    overall_info = (driving_info * int(weights_list[0]) + restaurant_info * int(weights_list[1]) + grocery_info * int(weights_list[2]) + hospital_info * int(weights_list[3]))/sum(int(i) for i in weights_list)
    commuting_info = {}
    for mode in mode_list:
        try:
            commuting_info[mode] = score_commuting(gmaps, start_address, target_address, mode)
        except IndexError as e:
            return render(request, 'error.html')
    # If nickname is specified, send nickname instead.
    if (start_nickname != ''):
        home_address= start_nickname
    
    if (target_nickname != ''):
        target_address = target_nickname

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

    if(request.user.is_authenticated):
        s1 = Search.objects.create(username = request.user.username, startAdd = start_address, startNick = start_nickname, 
        targetAdd = target_address, targetNick = target_nickname,
        overallScore = overall_info, driveScore = driving_info, restScore = restaurant_info, hospScore = hospital_info,
        groceryScore = grocery_info)


    # Mohana save to search database here
    #if(Search.objects.exists(startNick=start_nickname)):
    # s1 = Search.objects.filter(startNick=start_nickname) # can use get?
    # s1.overallScore = overall_info
    # s1.driveScore = commuting_info
    # s1.restScore = restaurant_info
    # s1.hospScore = hospital_info
    # s1.groceryScore = grocery_info
    # s1.save()

    #else:
        #return render(request, 'error.html')

    return render(request, 'rating.html', context = context)

def time_commuting_from_home_to_target(gmaps, source_address, target_address, mode):
    s_geocode_result = gmaps.geocode(source_address)
    t_geocode_result = gmaps.geocode(target_address)
    try:
        s_lat, s_lng, t_lat, t_lng = str(s_geocode_result[0]['geometry']['location']['lat']), str(s_geocode_result[0]['geometry']['location']['lng']), str(t_geocode_result[0]['geometry']['location']['lat']), str(t_geocode_result[0]['geometry']['location']['lng'])
    except IndexError as e:
        raise e
    # "https://maps.googleapis.com/maps/api/distancematrix/json?origins=40.6655101%2C-73.89188969999998&destinations=40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key=YOUR_API_KEY"
    result_list = []
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + s_lat + "%2C" + s_lng + "&destinations=" + t_lat + "%2C" + t_lng + "&key=AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc&mode=" + mode 
    response = requests.request("GET", url, headers = {}, data = {})
    est_time = response.json()['rows'][0]['elements'][0]['duration']['text']
    distance = response.json()['rows'][0]['elements'][0]['distance']['text']
    return (est_time, distance)

def score_nearby_restaurants(gmaps, home_address):
    try:
        num_of_restaurants, avg_rating = search_restaurant_near_home(gmaps, home_address)
    except IndexError as e:
        raise e
    score = log(0.1 * num_of_restaurants + 0.1) + avg_rating
    return round(score, 2)

def score_nearby_hospitals(gmaps, home_address):
    try:
        num_of_hospitals, avg_rating = search_hospital_near_home(gmaps, home_address)
    except IndexError as e:
        raise e
    score = log(0.1 * num_of_hospitals + 0.1) + avg_rating
    return round(score, 2)

def score_nearby_stores(gmaps, home_address):
    try:
        num_of_stores, avg_rating = search_grocery_store_near_home(gmaps, home_address)
    except IndexError as e:
        raise e
    score = log(0.1 * num_of_stores + 0.1) + avg_rating
    return round(score, 2)

def score_commuting(gmaps, home_address, targe_address, mode):
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
        return round(75 / time_in_minute, 2)
