#generates DB passenger_on_station_updated.csv
import pandas as pd
import random
from datetime import datetime, timedelta

# Define the time intervals
peak_intervals = timedelta(minutes=7.5)
nonpeak_intervals = timedelta(minutes=15)

# Define peak and non-peak hours
peak_hours = [(7, 8.5), (15, 18)]
nonpeak_hours = [(8.5, 15), (18, 19)]

# Define the stations
stations = [
    "Westmead", "Westmead Hospital", "Childrens Hospital", "Ngara", "Benaud Oval",
    "Fennel Street", "Prince Alfred Square", "Church Street", "Parramatta Square",
    "Robin Thomas", "Tramway Avenue", "Rosehill Gardens", "Yallamundi", "Dundas",
    "Telopea", "Carlingford"
]

# Calculate total intervals
start_time = datetime.strptime("07:00", "%H:%M")
end_time = datetime.strptime("19:00", "%H:%M")

total_intervals = 0
current_time = start_time

while current_time < end_time:
    hour = current_time.hour + current_time.minute / 60
    if any(start <= hour < end for start, end in peak_hours):
        interval = peak_intervals
    else:
        interval = nonpeak_intervals
    total_intervals += 1
    current_time += interval

# Initialize the list to store the data
data = []

# Set the maximum number of passengers
max_passengers = 28000

# Calculate total peak and non-peak intervals
current_time = start_time
total_peak_intervals = 0
total_nonpeak_intervals = 0

while current_time < end_time:
    hour = current_time.hour + current_time.minute / 60
    if any(start <= hour < end for start, end in peak_hours):
        total_peak_intervals += 1
    else:
        total_nonpeak_intervals += 1
    if any(start <= hour < end for start, end in peak_hours):
        interval = peak_intervals
    else:
        interval = nonpeak_intervals
    current_time += interval

# Allocate passengers
peak_passenger_allocation = 0.7 * max_passengers
nonpeak_passenger_allocation = 0.3 * max_passengers

# Special station passenger allocation
special_stations = {"Parramatta Square", "Prince Alfred Square", "Robin Thomas", "Church Street"}
special_station_allocation = 0.4  # 40% of passengers to special stations

# Calculate passengers per interval
passengers_per_peak_interval = peak_passenger_allocation / total_peak_intervals
passengers_per_nonpeak_interval = nonpeak_passenger_allocation / total_nonpeak_intervals

# Calculate passengers per station
special_station_passengers_peak = (special_station_allocation * passengers_per_peak_interval) / len(special_stations)
special_station_passengers_nonpeak = (special_station_allocation * passengers_per_nonpeak_interval) / len(special_stations)

regular_station_passengers_peak = (passengers_per_peak_interval - special_station_passengers_peak * len(special_stations)) / (len(stations) - len(special_stations))
regular_station_passengers_nonpeak = (passengers_per_nonpeak_interval - special_station_passengers_nonpeak * len(special_stations)) / (len(stations) - len(special_stations))

# Generate time intervals and passenger counts
current_time = start_time
total_passengers = 0

while current_time < end_time:
    hour = current_time.hour + current_time.minute / 60
    if any(start <= hour < end for start, end in peak_hours):
        interval = peak_intervals
        passengers_per_interval = passengers_per_peak_interval
        special_station_passengers = special_station_passengers_peak
        regular_station_passengers = regular_station_passengers_peak
    else:
        interval = nonpeak_intervals
        passengers_per_interval = passengers_per_nonpeak_interval
        special_station_passengers = special_station_passengers_nonpeak
        regular_station_passengers = regular_station_passengers_nonpeak
    
    for station in stations:
        if station in special_stations:
            passengers = special_station_passengers + random.randint(-10, 10)
        else:
            passengers = regular_station_passengers + random.randint(-10, 10)
        total_passengers += passengers
        data.append([current_time.strftime("%H:%M"), station, passengers])
    
    current_time += interval

# Adjust the total passengers to not exceed max_passengers
total_passenger_count = sum([x[2] for x in data])
adjustment_factor = max_passengers / total_passenger_count

for i in range(len(data)):
    data[i][2] = int(data[i][2] * adjustment_factor)

# Create a DataFrame and save to CSV
df = pd.DataFrame(data, columns=["time", "station", "passengers"])
df.to_csv("passenger_on_station_updated.csv", index=False)

print("CSV file has been created.")