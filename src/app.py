from src.simulation.simulation import Simulation
from src.model.city import City


def main():
    simulation = Simulation()
    city = City.from_numbers(22, 10).assign_bikes_randomly()

    temp = simulation.simulate(city, 30)


if __name__ == "__main__":
    main()
