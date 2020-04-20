from src.simulation.simulation import Simulation, time_of_number_of_days
from src.simulation.data_writer import ResultWriter
from src.model.city import City


def main():
    simulation = Simulation()
    city = City.from_numbers(600, 100).assign_bikes_randomly()

    time = time_of_number_of_days(7)
    simulation.simulate(city, time)

    ResultWriter.write_to_excel(simulation.get_stations_data(), "stations_states.xlsx")
    ResultWriter.write_to_excel(simulation.get_breaking_bikes_data(), "bikes_breaking.xlsx")


if __name__ == "__main__":
    main()
