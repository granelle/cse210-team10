import django
from django.test import TestCase
from django.test.client import RequestFactory
import googlemaps
from . import views
from unittest.mock import Mock, patch
import requests

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

 
class TestToolAPI(TestCase):
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
        self.assertEqual(views.time_commuting_from_home_to_target(mock_gmaps, "dummy_home_address", "dummy_target_address"), ("10 min", "3.1 miles"))
