import pandas as pd
import numpy as np
from tqdm import tqdm

from typing import List, Generator

from .bike_rental import BikeRental
from src.model import bike, city, station, listener, trip


class Simulation:

    def __init__(self):
        self.history_trips: List[trip.Trip] = []
        self.time_change_listeners: List[trip.Trip] = []

    def simulate(self, city: city.City, max_time: int, random_seed=997) -> pd.DataFrame:
        np.random.seed(random_seed)
        renting = BikeRental(city)

        for t in tqdm(range(max_time), "simulating"):
            print(f"time: {t}")
            new_trips = renting.simulate_bikes_renting(t)
            self.time_change_listeners.extend(new_trips)

            self.__time_changing(t)

        self.history_trips.extend(self.time_change_listeners)
        return self.history_trips

    def __time_changing(self, time: int) -> None:
        have_trips_ended = self.__call_listeners(time)
        for id, finished in enumerate(have_trips_ended):
            if finished:
                self.history_trips.append(self.time_change_listeners[id])
                del self.time_change_listeners[id]

    def __call_listeners(self, time: int) -> Generator[bool, None, None]:
        for listener in self.time_change_listeners:
            yield listener.on_time_change(time)
