import pandas as pd
import numpy as np
from tqdm import tqdm

from typing import List, Generator, Dict, Any

from .interface import BrokenBikesDataProvider, StationStatesDataProvider
from . import simulation_constants as constants
from .bike_rental import BikeRental
from src.model import bike, city, station, listener, trip


class Simulation(BrokenBikesDataProvider, StationStatesDataProvider):

    def __init__(self):

        self.history_trips: List[trip.Trip] = []
        self.time_change_listeners: List[trip.Trip] = []

        self.stations_states = []
        self.bikes_breaking = []

    def get_breaking_bikes_data(self) -> pd.DataFrame:
        breaking_bikes_columns = [constants.SimulationConstants.TIMESTAMP_LABEL,
                                  constants.SimulationConstants.BIKE_ID_LABEL]
        return pd.DataFrame(data=self.bikes_breaking, columns=breaking_bikes_columns)

    def get_stations_data(self) -> pd.DataFrame:
        stations_columns = [constants.SimulationConstants.TIMESTAMP_LABEL,
                            constants.SimulationConstants.STATION_ID_LABEL,
                            constants.SimulationConstants.BIKES_IDS_LABEL]
        return pd.DataFrame(data=self.stations_states, columns=stations_columns)

    def simulate(self, city: city.City, max_time: int, random_seed=997) -> List[trip.Trip]:
        self._validate_bikes(city.bikes)

        np.random.seed(random_seed)
        renting = BikeRental(city)

        for t in tqdm(range(max_time), "simulating"):
            # print(f"time: {t}")
            for s in city.stations:
                self.stations_states.append(self.__prepare_station_record(s, t))

            bikes_renting_generator = renting.simulate_bikes_renting(t)
            for trip, has_break in bikes_renting_generator:
                if has_break:
                    self.bikes_breaking.append(self.__prepare_bike_breaking_record_from_trip(trip, t))
                self.time_change_listeners.append(trip)
            # self.time_change_listeners.extend([trip for trip, time in bikes_renting_generator])

            self.__time_changing(t)

        return self

    def _validate_bikes(self, bikes: List[bike.Bike]):
        for bike in bikes:
            if not bike.is_valid:
                self.bikes_breaking.append(self.__prepare_bike_breaking_record(0, bike.bike_id))

    def __time_changing(self, time: int) -> None:
        """
        Simulate the change of time. Removes trips from active trips ``time_change_listeners`` list and append them to
        ``history_trips``.

        :param time: actual timestamp
        """
        have_trips_ended = list(self.__call_listeners(time))
        lasting_trips = []
        for id, finished in enumerate(have_trips_ended):
            if not finished:
                lasting_trips.append(self.time_change_listeners[id])
            else:
                self.history_trips.append(self.time_change_listeners[id])
        self.time_change_listeners = lasting_trips

    def __call_listeners(self, time: int) -> Generator[bool, None, None]:
        """
        Calls ``on_time_change`` for every trip
        :param time: actual time
        :return: True if the trip has just ended
        """
        for listener in self.time_change_listeners:
            yield listener.on_time_change(time)

    def __prepare_station_record(self, station: station.Station, timestamp: int) -> Dict[str, Any]:
        result = {
            constants.SimulationConstants.TIMESTAMP_LABEL: timestamp,
            constants.SimulationConstants.STATION_ID_LABEL: station.station_id,
            constants.SimulationConstants.BIKES_IDS_LABEL: set([b.bike_id for b in station.bikes])
        }
        return result

    def __prepare_bike_breaking_record_from_trip(self, trip: trip.Trip, time: int) -> Dict[str, Any]:
        return self.__prepare_bike_breaking_record(time, trip.bike.bike_id)

    def __prepare_bike_breaking_record(self, time: int, bike_id: int):
        res = {
            constants.SimulationConstants.TIMESTAMP_LABEL: time,
            constants.SimulationConstants.BIKE_ID_LABEL: bike_id
        }
        return res


def time_of_number_of_days(num_of_days):
    return num_of_days * 24 * int((60 / constants.TIME_STEP_MINS))
