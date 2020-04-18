from .bike import Bike
from .station import Station
from .listener import OnTimeChangeListener


class Trip(OnTimeChangeListener):

    # todo update stations

    def __init__(self, bike: Bike, end_time: int, from_station: Station, to_station: Station):
        self.bike = bike
        self.end_time = end_time
        self.from_station = from_station
        self.to_station = to_station

    @classmethod
    def from_start_time(cls, bike: Bike, start_time: int, duration: int,
                        from_station: Station, to_station: Station) -> 'Trip':
        end_time = start_time + duration
        return cls(bike, end_time, from_station, to_station)

    def start_trip(self) -> 'Trip':
        self.from_station.bike_leaves(self.bike)
        print(f"\tbike {self.bike.bike_id} leaves from {self.from_station.station_id} to {self.to_station.station_id} ({self.end_time})")
        self.bike.try_break_bike()
        return self

    def __end_trip(self):
        self.to_station.bike_arrives(self.bike)
        # todo increase bikes failure chance?

    def on_time_change(self, time: int) -> bool:
        if time == self.end_time:
            self.__end_trip()
            return True
        return False
