#! /usr/bin/python3

import unittest
from policy.google_maps_apis.geocode_apis import GeocodeApis

import googlemaps

from policy.tests.policy_test_common import PolicyTestCommon

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class TestGoogleGeolocation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PolicyTestCommon.test_class_init(cls, __name__)

    def setUp(self):
        pass
        # the db strategy implementations should have been initialized in
        # main()

    def tearDown(self):
        pass

    def test_Geocoding(self):
        """
        Connected to Google Maps and performs geocoding
        """

        # Reinaldo personal API Key...not to be abused
        geocodeApis = GeocodeApis()
        key = geocodeApis.find_gmaps_api_key()
        if key:
            gmaps = googlemaps.Client(key)
            # Geocoding an address
            geocode_result = gmaps.geocode(
                '170 West Tasman Dr., San Jose, CA 95134')
            self.assertIsNotNone(geocode_result)
            print(geocode_result[0]['formatted_address'])
            print(geocode_result[0]['geometry']['location']['lat'])
            print(geocode_result[0]['geometry']['location']['lng'])

            self.assertEqual(geocode_result[0]['formatted_address'],
                             "170 W Tasman Dr, San Jose, CA 95134, USA")
            self.assertEqual(
                geocode_result[0]['geometry']['location']['lat'], 37.4084383)
            self.assertEqual(
                geocode_result[0]['geometry']['location']['lng'], -121.9539644)

            # ChIJ9cdbI6_Jj4AReRg2NJUxLFA
            # https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=<YOUR_API_KEY>

        else:
            print("No Google Maps API KEY FOUND")

    def test_GeocodingZip(self):
        """
        Connected to Google Maps and performs geocoding
        """

        # Reinaldo personal API Key...not to be abused
        geocodeApis = GeocodeApis()
        key = geocodeApis.find_gmaps_api_key()
        if key:
            gmaps = googlemaps.Client(key)
            # Geocoding an address
            geocode_result = gmaps.geocode('95134')
            self.assertIsNotNone(geocode_result)
            print(geocode_result[0]['formatted_address'])
            print(geocode_result[0]['geometry']['location']['lat'])
            print(geocode_result[0]['geometry']['location']['lng'])

            self.assertEqual(geocode_result[0]['formatted_address'],
                             "San Jose, CA 95134, USA")
            self.assertEqual(
                geocode_result[0]['geometry']['location']['lat'], 37.4308503)
            self.assertEqual(
                geocode_result[0]['geometry']['location']['lng'], -121.9529992)
        else:
            print("No Google Maps API KEY FOUND")

    def test_GeocodingCity(self):
        """
        Connected to Google Maps and performs geocoding
        """

        # Reinaldo personal API Key...not to be abused
        geocodeApis = GeocodeApis()
        key = geocodeApis.find_gmaps_api_key()
        if key:
            gmaps = googlemaps.Client(key)

            # Geocoding an address

            geocode_result = gmaps.geocode('San Jose, CA')
            self.assertIsNotNone(geocode_result)
            print(geocode_result[0]['formatted_address'])
            print(geocode_result[0]['geometry']['location']['lat'])
            print(geocode_result[0]['geometry']['location']['lng'])

            self.assertEqual(
                geocode_result[0]['formatted_address'], "San Jose, CA, USA")
            self.assertEqual(
                geocode_result[0]['geometry']['location']['lat'], 37.3382082)
            self.assertEqual(
                geocode_result[0]['geometry']['location']['lng'], -121.8863286)
        else:
            print("No Google Maps API KEY found")    

    def test_ReverseGeocoding(self):
        """
        Connected to Google Maps and performs geocoding
        """

        # Reinaldo personal API Key...not to be abused
        geocodeApis = GeocodeApis()
        key = geocodeApis.find_gmaps_api_key()
        if key:
            gmaps = googlemaps.Client(key)

            # Look up an address with reverse geocoding
            reverse_geocode_result = gmaps.reverse_geocode(
                (37.4083511, -121.954079))
            self.assertIsNotNone(reverse_geocode_result)
            print(reverse_geocode_result[0]['formatted_address'])
            self.assertEqual(
                reverse_geocode_result[0]['formatted_address'],
                "Cisco Building D, 170 W Tasman Dr, San Jose, CA 95134, USA")
        else:
            print("No Google Maps API KEY found")

    def test_ReverseGeocodingFilter(self):
        """
        Connected to Google Maps and performs geocoding
        """

        # Reinaldo personal API Key...not to be abused
        geocodeApis = GeocodeApis()
        key = geocodeApis.find_gmaps_api_key()
        if key:
            gmaps = googlemaps.Client(key)
            # Look up an address with reverse geocoding
            reverse_geocode_result = gmaps.reverse_geocode(
                (37.4083511, -121.954079), result_type=['locality'])
            self.assertIsNotNone(reverse_geocode_result)
            self.assertEqual(reverse_geocode_result[0]['formatted_address'],
                             "San Jose, CA, USA") 
        else:
            print("No Google Maps API KEY found")

    def test_PlacesGeocoding(self):
        """
        Connected to Google Maps and performs geocoding
        """

        geocodeApis = GeocodeApis()
        key = geocodeApis.find_gmaps_api_key()
        if key:
            gmaps = googlemaps.Client(key)

            # Look up an address with reverse geocoding
            place_geocoding_result = gmaps.place('ChIJ9T_5iuTKj4ARe3GfygqMnbk')
            self.assertIsNotNone(place_geocoding_result)
            print(place_geocoding_result["result"]['formatted_address'])
            self.assertEqual(
                place_geocoding_result["result"]['formatted_address'],
                "San Jose, CA, USA")
        else:
            print("No Google Maps API KEY found")

    def test_GeofencingAlgo(self):
        """
        Connected to Google Maps and performs geocoding
        """

        geocodeApis = GeocodeApis()
        key = geocodeApis.find_gmaps_api_key()
        if key:
            gmaps = googlemaps.Client(key)

            geocode_result = gmaps.geocode('95134')
            place_id = geocode_result[0]["place_id"]
            types = geocode_result[0]['address_components'][0]['types']

            # Now let's suppose we get a notification for a certain lat, lng
            reverse_geocode_result = gmaps.reverse_geocode(
                (37.400281, -121.939455), result_type=types[0])

            if reverse_geocode_result[0]["place_id"] == place_id:
                print("client inside geofence")
            else:
                print("client outside geofence")
        else:
            print("No Google Maps API key found")
