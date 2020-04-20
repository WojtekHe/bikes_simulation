import pandas as pd

import abc


class StationStatesDataProvider(abc.ABC):

    @abc.abstractmethod
    def get_stations_data(self) -> pd.DataFrame:
        raise NotImplementedError()


class BrokenBikesDataProvider(abc.ABC):

    @abc.abstractmethod
    def get_breaking_bikes_data(self) -> pd.DataFrame:
        raise NotImplementedError()
