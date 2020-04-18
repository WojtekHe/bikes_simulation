import unittest

from src.model.city import City


class SimulationTest(unittest.TestCase):

    def test_init_from_numbers(self):
        num_bikes = 10
        num_stations = 3

        simulation = City.from_numbers(num_bikes, num_stations)

        self.assertEqual(len(simulation.stations), num_stations)
        self.assertEqual(len(simulation.bikes), num_bikes)
        self.assertEqual(simulation.bikes[-1].bike_id, num_bikes-1)
        self.assertEqual(simulation.stations[-1].station_id, num_stations-1)

    def test_assign_bikes_randomly_one_station(self):
        num_bikes = 10
        num_stations = 1

        city = City.from_numbers(num_bikes, num_stations).assign_bikes_randomly()

        expected_bikes_on_station = num_bikes
        actual_bikes = city.stations[0].bikes

        self.assertEqual(len(actual_bikes), expected_bikes_on_station)

    def test_assign_bikes_randomly_two_stations(self):
        num_bikes = 10
        num_stations = 2

        city = City.from_numbers(num_bikes, num_stations).assign_bikes_randomly()

        for station in city.stations:
            self.assertTrue(len(station.bikes) > 0)

