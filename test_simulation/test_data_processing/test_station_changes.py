import unittest

import pandas as pd

from src.data_processing.station_changes import StationChanges
from src.data_processing import processing_constants
from src.simulation import simulation_constants


class StationChangesTest(unittest.TestCase):

    def setUp(self) -> None:
        self.df = pd.DataFrame.from_dict({simulation_constants.SimulationConstants.BIKES_IDS_LABEL:
                                              [{1, 2, 3}, {2, 4}, {1, 3}, {4}],
                                          simulation_constants.SimulationConstants.STATION_ID_LABEL: [0, 1, 0, 1],
                                          simulation_constants.SimulationConstants.TIMESTAMP_LABEL: [0, 1, 1, 0]})

    def test_prepare_len_columns(self):
        test_values = {processing_constants.MOVED_COLUMN: {1},
                       processing_constants.ARRIVED_COLUMN: {2, 3, 4},
                       processing_constants.STAYED_COLUMN: {}}
        expected_new_values = {processing_constants.LEN_ARRIVED_COLUMN: 3,
                               processing_constants.LEN_STAYED_COLUMN: 0,
                               processing_constants.LEN_MOVED_COLUMN: 1}
        expected = test_values.copy()
        expected.update(expected_new_values)

        actual_values = StationChanges(self.df)._prepare_len_columns(test_values)

        self.assertDictEqual(expected, actual_values)

    def test_find_stations_changes(self):
        test_data = self.df

        expected = {processing_constants.STAYED_COLUMN: {0: {1, 3}, 1: {4}},
                    processing_constants.ARRIVED_COLUMN: {0: set(), 1: {2}},
                    processing_constants.MOVED_COLUMN: {0: {2}, 1: set()},
                    processing_constants.LEN_STAYED_COLUMN: {0: 2, 1: 1},
                    processing_constants.LEN_ARRIVED_COLUMN: {0: 0, 1: 1},
                    processing_constants.LEN_MOVED_COLUMN: {0: 1, 1: 0}}
        expected_df = pd.DataFrame.from_dict(expected)
        actual = StationChanges(test_data).find_stations_changes()

        pd.testing.assert_frame_equal(expected_df, actual)

