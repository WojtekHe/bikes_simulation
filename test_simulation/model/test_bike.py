import unittest

from src.model.bike import Bike

class BikeTest(unittest.TestCase):

    def test_bike_id(self):
        b1 = Bike()
        b2 = Bike()

        expected_b1_id = 1
        expected_b2_id = 2

        actual_b1_id = b1.bike_id
        actual_b2_id = b2.bike_id

        self.assertEqual(expected_b1_id, actual_b1_id)
        self.assertEqual(expected_b2_id, actual_b2_id)


