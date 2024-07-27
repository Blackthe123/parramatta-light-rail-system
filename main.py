# Importing pandas and some datetime libraries
import pandas as pd
from datetime import datetime, date, timedelta, time

# Load the tram timetable and convert time field into datetime
data = pd.read_csv('tram_timetable.csv')
data['time'] = pd.to_datetime(data['time'], format='%H:%M').dt.time

#Stations as per official NSW parramatta light rail website
stations = ["carlingford", "telopea", "dundas", "yallamundi", "rosehill gardens", 
            "tramway avenue", "robin thomas", "parramatta square", "church street",
            "prince alfred square", "fennel street", "benaud oval", "ngara", 
            "childrens hospital", "westmead hospital", "westmead"]

#Initialising variables used for time_input function parameters
start = "start"
end = "end"

#Function that asks for time input by the user and returns a time object
def time_input(when):
    while True:
        try:
            time_str = input(f"Enter {when} time (HH:MM): ")
            hour, minute = map(int, time_str.split(':'))
            if 7 <= hour <= 18 and 0 <= minute <= 59 and not (hour == 18 and minute >= 45):
                return time(hour, minute)
            print("Invalid time. Please enter a time between 07:00 and 18:44.")
        except ValueError:
            print("Invalid input. Please use HH:MM format.")

#Used for partial timetable generation where there is a start time and end time
def time_range_input():
    start_time = time_input(start)
    end_time = time_input(end)
    
    # Ensure start_time is before end_time
    if end_time < start_time:
        start_time, end_time = end_time, start_time
    
    return start_time, end_time

#Iterates through the tram_timetable DB; matches the time parameter to the record that has that time and appends tram number, time, and location from DB into the list that has been passed as a parameter
def appender(list1, time):
    for index, row in data.iterrows():
        if row['time'] == time:
            list1.append([row['tram_number'], time, row['location']])

#Called after the appender and checks if the "location" in the list is the station user inputted. This filters trams into possible trams that user can board.
def possible_tram_append(the_list, possible_list):
    for i in range(len(the_list)):
        if user_input_station in the_list[i]:
            possible_list.append(the_list[i])

#Feature 1)
def trip_planner():
    #Helping user pick a station
    print("Here are the stations you can choose from: ")
    print(stations)
    #User starting and destination location
    global user_input_station
    while True:
        user_input_station = input("Which station are you going to board the tram on? ").lower().strip()
        if user_input_station in stations:
            break    
    chosen_time = time_input(start)
    while True:
        user_destination = input("Where do you want to go? ").lower().strip()
        if user_destination in stations:
            break

    print("Time at which user is leaving: ", chosen_time)
    print("Station From: " + user_input_station)
    print("Station To: " + user_destination)

    #Variable Initialization
    list_equal = []
    list_after = []
    list_before = []
    list_after_after = []

    equality = False

    # Check if exact match for time input exists in DB
    for index, row in data.iterrows():
        if row['time'] == chosen_time:
            list_equal.append([row['tram_number'], chosen_time, row['location']])
            equality = True

    #If there is an exact match in DB. As per the question, we are finding 2 trams after the tram and 2 trams before the tram.
    if equality:
        #This tram arrives at the station user is on in the next interval. The for loop helps in figuring what time to pass into the appender subroutine.
        for index, row in data.iterrows():
            if row['time'] > chosen_time:
                after_equality = row["time"]
                break
        appender(list_after, after_equality) #See appender subroutine definition
                
        # This tram arrives at the station user is on after 2 intervals. The for loop helps in figuring what time to pass into the appender subroutine.
        for index, row in data.iterrows():
            if row['time'] > after_equality:
                after_after_equality = row["time"]
                break
        #Avoids index out of range errors
        if chosen_time < time(18, 30):
            appender(list_after_after, after_after_equality)
    else:
        # If exact match for usert time input not found in DB
        nearest_before = None
        nearest_after = None
        
        #Iterating through DB and initialising times to pass into appender subroutine
        for index, row in data.iterrows():
            if row['time'] < chosen_time:
                nearest_before = row['time']
            elif row['time'] > chosen_time:
                nearest_after = row['time']
                break
        
        #If the variables are not None and have a value
        if nearest_before:
            appender(list_equal, nearest_before)
        if nearest_after:
            appender(list_after, nearest_after)
                
        # Find the time before 'nearest_before'
        for index, row in data.iterrows():
            if row['time'] < nearest_before:
                before_nearest_before = row['time']
            else:
                break

        #Ensuring no index out of range errors
        if chosen_time >= time(7,7):
            appender(list_before, before_nearest_before)
                
        # Find the time after 'nearest_after'
        for index, row in data.iterrows():
            if row['time'] > nearest_after:
                after_nearest_after = row['time']
                break
        #Ensuring no index out of range errors
        if chosen_time < time(18, 30):
            appender(list_after_after, after_nearest_after)

    #Initialising lists
    list_possible_equal = []
    list_possible_after = []
    list_possible_before = []
    list_possible_after_after = []

    #See possible_tram_append subroutine dfinition
    possible_tram_append(list_equal, list_possible_equal)
    possible_tram_append(list_after, list_possible_after)
    possible_tram_append(list_before, list_possible_before)
    possible_tram_append(list_after_after, list_possible_after_after)

    #Combining all possible trams the user can board (2 time intervals after and two time intervals prior)
    all_possible_trams = list_possible_equal + list_possible_after + list_possible_before + list_possible_after_after

    # Create a dictionary to store different time calculations for each tram
    tram_travel_times = {}

    # unpacking index and item into i and tram
    for i, tram in enumerate(all_possible_trams):
        tram_number, tram_time = tram[0], tram[1]
        #calculates the wait time if the tram time is after the user's specified time; otherwise, the wait time is how much earlier the user has to arrive at the station
        if tram_time > chosen_time:
            wait_time = datetime.combine(date.today(), tram_time) - datetime.combine(date.today(), chosen_time)
        else:
            wait_time = datetime.combine(date.today(), chosen_time) - datetime.combine(date.today(), tram_time)
        
        all_possible_trams[i] = tram + [wait_time] #Giving each tram their wait time from calculations done above
        #Giving appropriate key value pairs for each tram
        tram_travel_times[tram_number] = {'wait_time': wait_time, 'departure_time': tram_time, 'arrival_time': None}

    # Calculate travel times, arrival time by matching trams from tram_travel_times, updating dictioary
    for index, row in data.iterrows():
        tram_number = row['tram_number'] #Assinment as per iteration
        if tram_number in tram_travel_times: #Checking if that particular tram is a "possible tram" which the user can board
            tram_info = tram_travel_times[tram_number] #Storing the data of that tram from the dictionary tram_travel_times
            if row['location'] == user_destination and row['time'] > tram_info['departure_time']:
                if tram_info['arrival_time'] is None:  # Only update if we havent found an arrival time yet
                    arrival_time = datetime.combine(date.today(), row['time'])
                    departure_time = datetime.combine(date.today(), tram_info['departure_time'])
                    travel_time = arrival_time - departure_time
                    tram_info['travel_time'] = travel_time
                    tram_info['arrival_time'] = row['time']

    # Update all_possible_trams with travel times
    for i, tram in enumerate(all_possible_trams):
        tram_number = tram[0]
        tram_info = tram_travel_times[tram_number]
        if tram_info['arrival_time'] is not None:
            all_possible_trams[i].append(tram_info['travel_time'])
        else:
            all_possible_trams[i].append(None)  # If tram doesnt arrive at destination before 18:45
    #Displaying data for each tram based on the calculations made above
    for tram_number, times in tram_travel_times.items():
        print(f"Tram {tram_number}:")
        print(f"  Departure time: {times['departure_time']}")
        print(f"  Arrival time: {times['arrival_time']}")
        print(f"  Wait time: {times['wait_time']}")
        print(f"  Travel time: {times.get('travel_time', 'N/A')}")
        if times['arrival_time'] is not None:
            print(f"  Total time: {times['travel_time'] + times['wait_time']}")
        print()

    #This function makes the system suggest a tram with the least total time taken for the entire journey
    def find_best_tram(tram_travel_times):
        best_tram = None
        best_total_time = timedelta.max #infinite time

        for tram_number, times in tram_travel_times.items():
            if times['arrival_time'] is not None:
                total_time = times['wait_time'] + times['travel_time']
                #Recyclying of best tram as it goes through
                if total_time < best_total_time:
                    best_total_time = total_time
                    best_tram = tram_number

        return best_tram

    # Find and display the best tram
    best_tram = find_best_tram(tram_travel_times)

    #Initialising variables that help in displaying all possible trams' timetables
    extra = None
    options = ['yes', 'no']

    #Displaying data of only the best tram separately
    if best_tram:
        best_tram_info = tram_travel_times[best_tram]
        print("\nBest Tram:")
        print(f"Tram Number: {best_tram}")
        print(f"Departure Time: {best_tram_info['departure_time']}")
        print(f"Wait Time: {best_tram_info['wait_time']}")
        print(f"Travel Time: {best_tram_info['travel_time']}")
        print(f"Arrival Time: {best_tram_info['arrival_time']}")
        print(f"Total Time: {best_tram_info['wait_time'] + best_tram_info['travel_time']}")
    else:
        print("No suitable tram found.")

    print("")
    print(f"Timetable for best tram: {best_tram}")
    print("################")
    # Find the index where the best tram starts its journey
    if best_tram is not None:
        start_index = data[(data['tram_number'] == best_tram) & (data['time'] == best_tram_info['departure_time'])].index[0]
        # Iterate through the timetable from the start index
        for i in range(start_index, len(data)):
            row = data.iloc[i]
            if row['tram_number'] == best_tram:
                print(row['time'], ":", row['location']) #Displaying timetable
                if row['time'] == best_tram_info['arrival_time']: #Stopping after destination is reached
                    break
        while extra not in options:
            print("Input Yes/No.")
            extra = input("Do you want to see the timetable for the other trams?").strip().lower() #Asking if user wants to see all trams he can take (2 intervals front and two intervals back as per question)
        if extra == "yes":
            for tram_number, times in tram_travel_times.items(): #Iterating through the dictionary that holds all possible trams
                if times['arrival_time'] is not None:
                    print(f"\nTimetable for tram {tram_number}:")
                    print("################")
                    # Find the index where the tram starts its journey
                    start_index = data[(data['tram_number'] == tram_number) & (data['time'] == times['departure_time'])].index[0]
                    # Iterate through the timetable from the start index
                    for i in range(start_index, len(data)):
                        row = data.iloc[i]
                        if row['tram_number'] == tram_number:
                            print(row['time'], ":", row['location']) #Displaying timetable
                            if row['time'] == times['arrival_time']: #Stopping after destination is reached
                                break

#Feature 2)
def passenger():
    chosen_time = time_input(start)
    #Loading passenger_data DB
    passenger_df = pd.read_csv('passenger_on_stations_updated.csv')
    passenger_df['time'] = pd.to_datetime(passenger_df['time'], format='%H:%M').dt.time
    
    #Matching the input time to one in the DB
    if chosen_time not in data['time'].values:
        chosen_time = min(data['time'][data['time'] > chosen_time])

    # Adhering to project parameters. Non peak hours passengr on board each tram is 200. Peak hours it is 400.
    if chosen_time <= time(8, 30) or (chosen_time >= time(15, 0) and chosen_time <= time(18, 0)):
        passengers_onboard = 400
    else:
        passengers_onboard = 200
    
    #Displaying passengers onboard for each tram
    print("Passengers Onboard")
    for i in range(1, 17):
        print(f"tram {i} : {passengers_onboard}")

    print("#############")

    #Using passenger_data DB to display passengers boarding
    for index, row in data.iterrows():
        if row['time'] == chosen_time:
            print("tram " + str(row["tram_number"]) + " station : " + row["location"])
            for index1, row1 in passenger_df.iterrows():
                if row1['time'] == chosen_time and row1['station'].lower() == row["location"]:
                    print("tram " + str(row["tram_number"]) + " boarding : " + str(row1["passengers"]))
#Feature 3)
def tram_deployment_details():
    user_time = time_input(start)
    #Matching the input time to one in the DB
    if user_time not in data['time'].values:
        user_time = min(data['time'][data['time'] > user_time])
    
    #Displaying Trma_deployment details
    print("There are 16 trams running at this instant. 8 trams on either track. 8 going toward Carlingford. 8 going towards Westmead. Below is a specific list of each tram and the station they are heading towards:")
    for index, row in data.iterrows():
        if row['time'] == user_time:
            print("tram " + str(row["tram_number"]) + "     station : " + row["location"])


#Feature 4)
def partial_gen():
    # Get the start and end times from the user
    chosen_time_start, chosen_time_end = time_range_input()

    # Filter the tram data based on the user input times
    filtered_trams = data[(data['time'] >= chosen_time_start) & (data['time'] <= chosen_time_end)]

    # Print the filtered tram timetable information
    for index, row in filtered_trams.iterrows():
        print(f"Tram {row['tram_number']} : {row['time']} : {row['location']}")

    print("#############")

#Feature 5)
def full_gen():
    tram_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]
    given_tram = None
    #Ensures valid tram number is given
    while given_tram not in tram_list:
        print("Please enter a number from 1-16. There are 16 trams in this light rail system.")
        given_tram = input("Which tram's timetable do you want to generate? ").strip()

    #Diplays entire timetable of the tram
    for index, row in data.iterrows():
        if row['tram_number'] == int(given_tram):
            print(str(row["time"]) + " : " + row["location"])

#Initialization for the main loop
input_error = ["1", "2", "3", "4", "5", "6"]
main_question = None

#Welcoming the user
print("Welcome to the Parramatta light rail system!")
print("")
#main loop: It keeps on asking main question until user decides to quit. It calls the respective functions depending on user input
while True:
    while main_question not in input_error:
        print("Please enter either 1, 2, 3, 4, 5, or 6")
        main_question = input("1) Trip planner  2) Passenger data  3) Tram Deployment Details  4) Partial timetable genration  5) Complete timetable generation  6) Quit\n").strip()
    if main_question == "1":
        trip_planner()
    elif main_question == "2":       
        passenger()
    elif main_question == "3":
        tram_deployment_details()
    elif main_question == "4":
        partial_gen()
    elif main_question == "5":
        full_gen()
    elif main_question == "6":
        break
    main_question = None #Question is asked again