import pandas as pd
from tqdm import tqdm

from typing import Generator, List, Any, Iterable

from . import processing_constants
from src.simulation.simulation_constants import SimulationConstants


class BikesScoring:

    def __init__(self, data: pd.DataFrame) -> None:
        self.df = data

    def score_bikes(self):
        """
        out:

           * index: (SimulationConstants.BIKE_ID_LABEL, SimulationConstants.TIMESTAMP_LABEL)
           * values: [plus, minus]

        :return: out
        """
        out_df = pd.DataFrame(data=self._collect_results(),
                              columns=[SimulationConstants.BIKE_ID_LABEL, SimulationConstants.TIMESTAMP_LABEL,
                                       processing_constants.PLUS_LABEL, processing_constants.MINUS_LABEL])

        return out_df

    def _collect_results(self):
        accumulator = []
        tqdm.pandas(desc="scoring bikes")
        for scores in self.df.progress_apply(lambda x: BikesScoring._score_record(x), axis=1):
            accumulator.extend(list(scores))
        return accumulator

    @staticmethod
    def _score_record(record: pd.Series) -> Iterable[List[Any]]:
        """
        yields a data with format accurate to score_bikes ``out``: BIKE_ID_LABEL, TIMESTAMP_LABEL, plus, minus

        :param record: single row of ``self.df``
        :return: processed record for scoring bikes; order: BIKE_ID_LABEL, TIMESTAMP_LABEL, plus, minus
        """
        minus = list(BikesScoring._score_record_minus(record))
        plus = list(BikesScoring._score_record_plus(record))

        joined = []
        joined.extend(minus)
        joined.extend(plus)
        return joined

    @staticmethod
    def _score_record_minus(record: pd.Series) -> Generator[List[Any], None, None]:
        if record[processing_constants.LEN_MOVED_COLUMN] > 0:
            divide_by = record[processing_constants.LEN_STAYED_COLUMN] + record[processing_constants.LEN_MOVED_COLUMN]
            for stayed_bike_id in record[processing_constants.STAYED_COLUMN]:
                yield [stayed_bike_id, record[SimulationConstants.TIMESTAMP_LABEL], 0, 1.0 / divide_by]

    @staticmethod
    def _score_record_plus(record: pd.Series) -> Generator[List[Any], None, None]:
        for moved_bike_id in record[processing_constants.MOVED_COLUMN]:
            yield [moved_bike_id, record[SimulationConstants.TIMESTAMP_LABEL], 1, 0]
