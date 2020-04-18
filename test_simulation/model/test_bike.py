import unittest

from src.model.bike import Bike
from src.model.constants import BIKE_BREAKING_BASE_CHANCE

class BikeTest(unittest.TestCase):

    def test_try_breaking_break(self):

        bike = Bike(1)
        chance = 0

        actual_is_valid = bike.try_break_bike(chance)

        self.assertFalse(actual_is_valid)

    def test_try_breaking_not_break(self):

        bike = Bike(1)
        chance = 1
        expected_breaking_chance = 2*BIKE_BREAKING_BASE_CHANCE

        actual_is_valid = bike.try_break_bike(chance)
        actual_breaking_chance = bike.breaking_chance

        self.assertTrue(actual_is_valid)
        self.assertEqual(expected_breaking_chance, actual_breaking_chance)



