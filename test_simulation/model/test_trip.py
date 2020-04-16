import unittest

from src.model.station import Station
from src.model.trip import Trip

class TripTest(unittest.TestCase):

    def test_trip_from_start_time(self):

        t = Trip.from_start_time(None, 10, 5)
        expected_end_time = 10+5
        actual_end_time = t.end_time

        self.assertEqual(expected_end_time, actual_end_time)


