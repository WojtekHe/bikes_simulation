import unittest

from src.model.city import City
from src.simulation.simulation import Simulation, time_of_number_of_days
from src.data_processing import bikes_scoring, station_changes, processing_constants


class AppTest(unittest.TestCase):
    def test_working(self):
        city = City.from_numbers(100, 10).assign_bikes_randomly()
        time = time_of_number_of_days(3)
        simulaiton = Simulation()

        simulaiton.simulate(city, time)

        broken_bikes = simulaiton.get_breaking_bikes_data()
        trips_history = simulaiton.get_stations_data()

        res_stations_changes = station_changes.StationChanges(trips_history).find_stations_changes()
        scores = bikes_scoring.BikesScoring(res_stations_changes).score_bikes()
