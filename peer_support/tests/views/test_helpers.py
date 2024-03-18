from django.test import TestCase
from peer_support.views.helpers import country_to_continent, country_to_continent_specific

class TestCountryToContinent(TestCase):
    """Unit test of country code converter"""

    def test_country_to_continent_known(self):
        self.assertEqual(country_to_continent('US'), 'North America')

    def test_country_to_continent_unknown(self):
        self.assertEqual(country_to_continent('XX'), 'Unknown') 

    def test_country_to_continent_two_known(self):
        self.assertEqual(country_to_continent_specific('US'), ('North America', 'United States'))

    def test_country_to_continent_two_unknown(self):
        self.assertEqual(country_to_continent_specific('XX'), ('Unknown', 'Unknown'))
