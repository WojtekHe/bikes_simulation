import numpy as np

from typing import List

from .bike import Bike
from .station import Station


class City:

    def __init__(self, bikes: List[Bike], stations: List[Station]) -> None:
        self.bikes = bikes
        self.stations = stations

    @classmethod
    def from_numbers(cls, num_bikes: int, num_stations: int) -> "City":
        bikes = cls.__generate_bikes(num_bikes)
        stations = cls.__generate_stations(num_stations)
        return cls(bikes, stations)

    @staticmethod
    def __generate_bikes(num_bikes: int) -> List[Bike]:
        bikes = []
        for bike_id in range(num_bikes):
            bikes.append(Bike(bike_id))
        return bikes

    @staticmethod
    def __generate_stations(num_stations: int) -> List[Station]:
        stations = []
        for station_id in range(num_stations):
            stations.append(Station(station_id))
        return stations

    def assign_bikes_randomly(self, random_seed=997):
        np.random.seed(random_seed)
        for bike in self.bikes:
            self.stations[np.random.randint(0, len(self.stations))].bikes.append(bike)
        return self

    def make_n_bikes_broken(self, n):
        for i in range(n):
            self.bikes[i].is_valid = False

        return self
