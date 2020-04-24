import unittest

import pandas as pd

from src.data_processing import processing_constants
from src.simulation.simulation_constants import SimulationConstants
from src.data_processing.bikes_scoring import BikesScoring, BikesChecking

class BikesScoringTest(unittest.TestCase):

    def setUp(self) -> None:
        self.df = pd.DataFrame.from_dict({SimulationConstants.TIMESTAMP_LABEL: [1, 2],
                                          SimulationConstants.STATION_ID_LABEL: [0, 0],
                                          processing_constants.STAYED_COLUMN: [{1, 3}, {1, 3}],
                                          processing_constants.LEN_STAYED_COLUMN: [2, 2],
                                          processing_constants.ARRIVED_COLUMN: [{}, {4}],
                                          processing_constants.LEN_ARRIVED_COLUMN: [0, 1],
                                          processing_constants.MOVED_COLUMN: [{2, 99}, {}],
                                          processing_constants.LEN_MOVED_COLUMN: [2, 0]})

    def test_score_record_minus(self):
        record = self.df.iloc[0]

        # order: bike_id, time, plus, minus
        expected_values = [[1, 1, 0, 1 / 4], [3, 1, 0, 1 / 4]]
        actual_values = list(BikesScoring._score_record_minus(record))

        self.assertListEqual(expected_values, actual_values)

    def test_score_record_plus(self):
        record = self.df.iloc[0]

        # order: bike_id, time, plus, minus
        expected_values = [[2, 1, 1, 0], [99, 1, 1, 0]]
        actual_values = list(BikesScoring._score_record_plus(record))

        self.assertListEqual(expected_values, actual_values)

    def test_score_record(self):
        record = self.df.iloc[0]

        expected_values = [[1, 1, 0, 1 / 4], [3, 1, 0, 1 / 4], [2, 1, 1, 0], [99, 1, 1, 0]]
        actual_values = list(BikesScoring._score_record(record))

        self.assertListEqual(expected_values, actual_values)

    def test_score_bikes(self):
        # order: bike_id, time, plus, minus
        expected_values = [[1, 1, 0, 1 / 4], [3, 1, 0, 1 / 4], [2, 1, 1, 0], [99, 1, 1, 0]]
        actual_values = BikesScoring(self.df).score_bikes().values.tolist()

        self.assertListEqual(expected_values, actual_values)


class BikesCheckingTest(unittest.TestCase):

    def setUp(self) -> None:
        self.all_bikes = [1, 2, 3, 4, 5]
        self.broken_bikes = pd.DataFrame.from_dict({SimulationConstants.TIMESTAMP_LABEL: [2, 5],
                                                    SimulationConstants.BIKE_ID_LABEL: [1, 4]})
        self.checking = BikesChecking(self.broken_bikes, self.all_bikes)

    def test_broken_bikes_for_time2(self):
        time = 2
        expected_broken_bikes = [1]

        actual_broken_bikes = self.checking.broken_bikes_for_time(time).values.tolist()

        self.assertListEqual(expected_broken_bikes, actual_broken_bikes)

    def test_broken_bikes_for_time3(self):
        time = 3
        expected_broken_bikes = [1]

        actual_broken_bikes = self.checking.broken_bikes_for_time(time).values.tolist()

        self.assertListEqual(expected_broken_bikes, actual_broken_bikes)

    def test_broken_bikes_for_time5(self):
        time = 5
        expected_broken_bikes = [1, 4]

        actual_broken_bikes = self.checking.broken_bikes_for_time(time).values.tolist()

        self.assertListEqual(expected_broken_bikes, actual_broken_bikes)

    def test_bikes_states(self):
        time = 2
        expected_states = {1: False, 2: True, 3: True, 4: True, 5: True}

        actual_states = self.checking.bikes_states(time).to_dict()

        self.assertDictEqual(expected_states, actual_states)