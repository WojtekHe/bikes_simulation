from .constants import BIKE_BREAKING_BASE_CHANCE


class Bike:

    __num_bikes = 0

    def __init__(self, bike_id):
        self.bike_id = bike_id
        self.is_valid = True
        self.breaking_chance = BIKE_BREAKING_BASE_CHANCE

    def break_bike(self) -> 'Bike':
        self.is_valid = False
        return self
