from typing import List

from .bike import Bike


class Station:

    def __init__(self, station_id):
        self.station_id = station_id
        self.bikes = []

    def append_bikes(self, bikes: List[Bike]) -> 'Station':
        self.bikes.append(bikes)
        return self

    def bike_leaves(self, bike: Bike) -> 'Station':
        self.bikes.remove(bike)
        return self

    def bike_arrives(self, bike: Bike) -> 'Station':
        self.bikes.append(bike)
        return self
