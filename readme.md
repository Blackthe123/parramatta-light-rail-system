# Parramatta Light Rail Project

This project simulates and manages the operations of the Parramatta Light Rail system. It includes features for trip planning, passenger data management, tram deployment details, and timetable generation. There are 16 trams and 16 stations: "carlingford", "telopea", "dundas", "yallamundi", "rosehill gardens", "tramway avenue", "robin thomas", "parramatta square", "church street", "prince alfred square", "fennel street", "benaud oval", "ngara", "childrens hospital", "westmead hospital", "westmead".

## Features

### `main.py`
The main script includes the following features:
1. **Trip Planner**: Helps users plan their trips by suggesting the best trams based on their input time and location.
2. **Passenger Data Management**: Manages data related to passenger boarding and onboard details.
3. **Tram Deployment Details**: Provides information about tram deployment and scheduling.
4. **Partial Timetable Generation**: Generates partial timetables based on specific criteria.
5. **Full Timetable Generation**: Generates comprehensive timetables for the entire tram network.

### CSV File Generators
- **`passenger_on_station_gen.py`**: Generates data for passenger boarding at different stations.
- **`tram_timetable_gen.py`**: Generates tram timetable data.

## Included Files
- `main.py`: The main script with core functionalities.
- `passenger_on_station_gen.py`: Script to generate passenger data.
- `passenger_on_stations_updated.csv`: Example CSV file with passenger data.
- `tram_timetable.csv`: Example CSV file with tram timetable data.
- `tram_timetable_gen.py`: Script to generate tram timetable data.

## Usage
1. **Trip Planning**: Use the trip planner feature in `main.py` to find the best trams based on your input time and location.
2. **Passenger Data Management**: Track and manage passenger boarding and onboard data using `passenger_on_station_gen.py`.
3. **Timetable Generation**: Use `tram_timetable_gen.py` to generate full or partial tram timetables based on your requirements.

## Community Use
This project can be utilized by the community in several ways:
1. **Simulation and Analysis**: Use the generated data to simulate and analyze tram operations and passenger flow.
2. **Educational Purposes**: Serve as a learning tool for those studying transportation systems and data management.
3. **Feature Expansion**: Build upon the existing features to add more functionalities or adapt it to other transportation systems.
4. **Research**: Utilize the data for research in urban planning, transportation logistics, and related fields.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests with your improvements and features.
