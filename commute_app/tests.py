import django
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from commute_app.models import Search
import factory
import googlemaps
from . import views
from unittest.mock import Mock, patch
import requests

# Mock nearby responses.
class MockNearbyResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            'results':[
                {'rating': 4.5},
                {'rating': 4.1}
            ]
        }

# Mock commute responses.
class MockCommuteResponse:
    def __init__(self):
        self.status_code = 200
    
    def json(self):
        return{
            'rows': [
                {
                    'elements': [
                        {
                            'duration': {
                                'text': "10 min"
                            },
                            'distance': {
                                'text': "3.1 miles"
                            }
                        }
                    ]
                }
            ]
        }

# Test search functionality for API.
class TestSearchAPI(TestCase):
    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockNearbyResponse())
    def test_restaurant(self, mock_response, mock_gmaps):
        self.assertEqual(views.search_restaurant_near_home(mock_gmaps, 'dummy_home_address'), (2, 4.3))

    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockNearbyResponse())
    def test_hospital(self, mock_response, mock_gmaps):
        self.assertEqual(views.search_hospital_near_home(mock_gmaps, 'dummy_home_address'), (2, 4.3))

    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockNearbyResponse())
    def test_grocery_store(self, mock_response, mock_gmaps):
        self.assertEqual(views.search_grocery_store_near_home(mock_gmaps, 'dummy_home_address'), (2, 4.3))

    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockCommuteResponse())
    def test_commute(self, mock_response, mock_gmaps):
        self.assertEqual(views.time_commuting_from_home_to_target(mock_gmaps, "dummy_home_address", "dummy_target_address", 'dummy_mode'), ("10 min", "3.1 miles"))

# Class for testing score calculations.
class TestScoreAPI(TestCase):
    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockCommuteResponse())
    @patch('commute_app.views.search_restaurant_near_home', return_value = (5, 3))
    def test_score_nearby_restaurants(self, mock_response, mock_gmaps, mock_search):
        self.assertEqual(views.score_nearby_restaurants(mock_gmaps, 'dummy_home_address'), 2.49)

    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockCommuteResponse())
    @patch('commute_app.views.search_hospital_near_home', return_value = (4, 2))
    def test_score_nearby_hospitals(self, mock_response, mock_gmaps, mock_search):
        self.assertEqual(views.score_nearby_hospitals(mock_gmaps, 'dummy_home_address'), 1.31)

    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockCommuteResponse())
    @patch('commute_app.views.search_grocery_store_near_home', return_value = (6, 4))
    def test_score_nearby_grocery_stores(self, mock_response, mock_gmaps, mock_search):
        self.assertEqual(views.score_nearby_stores(mock_gmaps, 'dummy_home_address'), 3.64)

    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockCommuteResponse())
    @patch('commute_app.views.time_commuting_from_home_to_target', return_value = ('30 mins', []))
    def test_score_commuting_long_minutes(self, mock_response, mock_gmaps, mock_search):
        self.assertEqual(views.score_commuting(mock_gmaps, 'dummy_home_address', 'dummy_target_address', 'driving'), 2.5)

    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockCommuteResponse())
    @patch('commute_app.views.time_commuting_from_home_to_target', return_value = ('3 hours 24 mins', []))
    def test_score_commuting_hours(self, mock_response, mock_gmaps, mock_search):
        self.assertEqual(views.score_commuting(mock_gmaps, 'dummy_home_address', 'dummy_target_address', 'driving'), 0.37)

    @patch("googlemaps.Client")
    @patch("requests.request", return_value = MockCommuteResponse())
    @patch('commute_app.views.time_commuting_from_home_to_target', return_value = ('1 day 8 hours 24 mins', []))
    def test_score_commuting_days(self, mock_response, mock_gmaps, mock_search):
        self.assertEqual(views.score_commuting(mock_gmaps, 'dummy_home_address', 'dummy_target_address', 'driving'), 0.04)

# Test Search model.
class TestSearchModel(TestCase):
    def createSearchFactory(self, username = 'Tim Jang', startAdd = 'UCSD', startNick = 'Home', targetAdd = 'Los Angeles', targetNick = 'School', date = None, overallScore = 4.5, driveScore = 3.5, restScore = 2.4, hospScore = 3.3, groceryScore = 2.4):
        return Search.objects.create(username=username, startAdd=startAdd, startNick=startNick, targetAdd=targetAdd, targetNick=targetNick, date=date, overallScore=overallScore, driveScore=driveScore, restScore=restScore, hospScore=hospScore, groceryScore=groceryScore)

    def test_cerate_model(self):
        searchModel = self.createSearchFactory()
        self.assertTrue(isinstance(searchModel, Search))
        self.assertEqual(searchModel.__str__(), searchModel.username)

# Test logging into the website.
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'username',
            'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/login/', self.credentials)
        self.assertTrue(type(response), django.http.response)