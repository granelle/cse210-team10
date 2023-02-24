import django
from django.test import TestCase
from django.test.client import RequestFactory
import googlemaps
from . import views

# Perform tests on Google API used in backend for searching.
class SearchTest(TestCase):
    # Test search_restaurant_near_home.
    def test_restaurants_near_home(self):
        gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
        home_address='3869 Miramar St, La Jolla, CA'
        out = views.search_restaurant_near_home(gmaps, home_address)
        self.assertEquals(out[0], 20)
        self.assertAlmostEquals(out[1], 4.050000000000001, 0)

    # Test search_hospital_near_home.
    def test_search_hospital_near_home(self):
        gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
        home_address='3869 Miramar St, La Jolla, CA'
        out = views.search_hospital_near_home(gmaps, home_address)
        self.assertEquals(out[0], 20)
        self.assertAlmostEquals(out[1], 2.1550000000000002, 0)

    # Test search_grocery_store_near_home.
    def test_search_grocery_store_near_home(self):
        gmaps = googlemaps.Client(key='AIzaSyDlgbzrdKouAchIHAfHog63OYtqkf0RPoc')
        home_address='3869 Miramar St, La Jolla, CA'
        out = views.search_grocery_store_near_home(gmaps, home_address)
        self.assertEquals(out[0], 2)
        self.assertAlmostEquals(out[1], 4.5, 0)

    # Test search_near_home.
    def test_search_near_home(self):
        # Create mock request.
        rf = RequestFactory()
        get_request = rf.get('/hello/')
        out = views.search_near_home(get_request)
        self.assertEquals(type(out), django.http.response.HttpResponse)