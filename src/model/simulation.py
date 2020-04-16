from .bike import Bike
from .station import Station
from .trip import Trip
from .listener import OnTimeChangeListener


class Simulation:

    def __init__(self, bikes, stations):
        self.bikes = bikes
        self.stations = stations

    @classmethod
    def from_numbers(cls, num_bikes, num_stations):
        bikes = cls.generate_bikes(num_bikes)
        stations = cls.generate_stations(num_stations)
        return cls(bikes, stations)

    @staticmethod
    def generate_bikes(num_bikes):
        bikes = []
        for bike_id in range(num_bikes):
            bikes.append(Bike(bike_id))
        return bikes

    @staticmethod
    def generate_stations(num_stations):
        stations = []
        for station_id in range(num_stations):
            stations.append(Station(station_id))
        return stations

