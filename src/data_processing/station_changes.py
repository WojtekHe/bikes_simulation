import pandas as pd
from tqdm import tqdm

from typing import Dict, Any

from . import processing_constants
from ..simulation import simulation_constants


class StationChanges:

    def __init__(self, history: pd.DataFrame) -> None:
        """
         df scheme:

           * TIMESTAMP_LABEL = "timestamp"
           * STATION_ID_LABEL = "station_id"
           * BIKES_IDS_LABEL = "bikes_ids"

        """
        self.df = history.sort_values(by=[simulation_constants.SimulationConstants.TIMESTAMP_LABEL])

    def find_stations_changes(self):
        """
        out - pd.DataFrame with columns:

           * SimulationConstants.TIMESTAMP_LABEL -> "timestamp"
           * SimulationConstants.STATION_ID_LABEL -> "station_id"
           * processing_constants.STAYED_COLUMN -> ("stayed")
           * processing_constants.ARRIVED_COLUMN -> ("arrived")
           * processing_constants.MOVED_COLUMN -> ("moved")
           * processing_constants.LEN_STAYED_COLUMN -> len("stayed")
           * processing_constants.LEN_ARRIVED_COLUMN -> len("arrived")
           * processing_constants.LEN_MOVED_COLUMN -> len("moved")

        :return:
        """
        out = []
        tqdm.pandas()

        for station in tqdm(self.df[simulation_constants.SimulationConstants.STATION_ID_LABEL].unique(),
                            "finding stations changes"):
            df_temp = self.df[self.df[simulation_constants.SimulationConstants.STATION_ID_LABEL] == station]\
                .reset_index(drop=True)

            for idx, row_values in enumerate(df_temp.values):
                time, station_id, set_ = row_values
                try:
                    prev = df_temp[simulation_constants.SimulationConstants.BIKES_IDS_LABEL].loc[idx - 1]
                except KeyError:
                    pass
                else:
                    res = {simulation_constants.SimulationConstants.TIMESTAMP_LABEL: time,
                           simulation_constants.SimulationConstants.STATION_ID_LABEL: station_id,
                           processing_constants.STAYED_COLUMN: set_ & prev,
                           processing_constants.ARRIVED_COLUMN: set_ - prev,
                           processing_constants.MOVED_COLUMN: prev - set_}

                    out.append(self._prepare_len_columns(res))

        return pd.DataFrame(out)

    @staticmethod
    def _prepare_len_columns(data_dict: Dict[str, Any]) -> Dict[str, Any]:
        temp = {}
        for k, v in [(k, v) for k, v in data_dict.items() if k in processing_constants.LEN_MAPPING.keys()]:
            temp[processing_constants.LEN_MAPPING[k]] = len(v)

        data_dict.update(temp)
        return data_dict
