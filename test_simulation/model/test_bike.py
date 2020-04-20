import unittest
from unittest.mock import patch

from src.model.bike import Bike
from src.model.constants import BIKE_BREAKING_BASE_CHANCE, BIKE_BREAKING_INCREASE


class BikeTest(unittest.TestCase):

    @patch("numpy.random.random")
    def test_try_breaking_break(self, mock_random):
        mock_random.return_value = 1

        bike = Bike(1)

        has_been_broken = bike.try_break_bike()

        self.assertTrue(has_been_broken)

    @patch("numpy.random.random")
    def test_try_breaking_not_break(self, mock_random):
        mock_random.return_value = 0

        bike = Bike(1)
        expected_breaking_chance = BIKE_BREAKING_BASE_CHANCE + BIKE_BREAKING_INCREASE

        actual_has_been_broken = bike.try_break_bike()
        actual_breaking_chance = bike.breaking_chance

        self.assertFalse(actual_has_been_broken)
        self.assertEqual(expected_breaking_chance, actual_breaking_chance)



