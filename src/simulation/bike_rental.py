import numpy as np

from typing import Tuple, Generator

from . import simulation_constants as constants

from src.model.bike import Bike
from src.model.city import City
from src.model.station import Station
from src.model.trip import Trip


class BikeRental:

    def __init__(self, city: City, random_seed=1997) -> None:
        self.city = city
        np.random.seed(random_seed)

    def simulate_bikes_renting(self, actual_time) -> Generator[Tuple[Trip, bool], None, None]:
        for bike, station in self.__find_bike():
            duration = self.__generate_trip_duration()
            destination = self.__find_destination_station()
            trip = Trip.from_start_time(bike, actual_time, duration, station, destination)
            yield trip, trip.start_trip()

    def __find_bike(self) -> Generator[Tuple[Bike, Station], None, None]:
        for station in self.city.stations:
            for bike in station.bikes:
                chance = 1 - np.random.random()
                broken_bike_penalty = 1 if bike.is_valid else constants.BROKEN_BIKE_RENTAL_PENALTY

                final_bike_rental_chance = constants.BIKE_RENTAL_CHANCE * broken_bike_penalty

                if chance <= final_bike_rental_chance:
                    yield bike, station

    def __find_destination_station(self) -> Station:
        num_stations = len(self.city.stations)
        random_station_id = np.random.randint(0, num_stations)

        return self.city.stations[random_station_id]

    def __generate_trip_duration(self):
        duration = np.random.poisson(lam=constants.POISSON_LAMBDA_TRIP_DURATION)
        return duration


