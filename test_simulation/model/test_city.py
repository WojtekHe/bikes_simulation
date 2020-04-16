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


