from django.test import TestCase
from django.urls import reverse
import googlemaps
from . import views

# Create your tests here.
class SearchTest(TestCase):
    # Test search_restaurant_near_home.
    def test_restaurants_near_home(self):
        gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
        home_address='3869 Miramar St, La Jolla, CA'
        out = views.search_restaurant_near_home(gmaps, home_address)
        self.assertEquals(out, (20, 4.050000000000001))