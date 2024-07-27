#generates tram_timetable DB
from datetime import datetime, timedelta

class Station:
    def __init__(self, name):
        self.name = name

class Tram:
    def __init__(self, id, start_station, direction):
        self.id = id
        self.timetable = []
        self.current_station_index = start_station
        self.direction = direction  # 1 for Carlingford to Westmead, -1 for Westmead to Carlingford

    def add_stop(self, time, station):
        self.timetable.append((time, station))

class TramSystem:
    def __init__(self):
        self.stations = [
            Station("Carlingford"), Station("Telopea"), Station("Dundas"),
            Station("Yallamundi"), Station("Rosehill Gardens"), Station("Tramway Avenue"),
            Station("Robin Thomas"), Station("Parramatta Square"), Station("Church Street"),
            Station("Prince Alfred Square"), Station("Fennel Street"), Station("Benaud Oval"),
            Station("Ngara"), Station("Childrens Hospital"), Station("Westmead Hospital"),
            Station("Westmead")
        ]
        self.trams = [
            Tram(1, 0, 1), Tram(2, 2, 1), Tram(3, 4, 1), Tram(4, 6, 1), Tram(5, 8, 1), 
            Tram(6, 10, 1), Tram(7, 12, 1), Tram(8, 15, -1), Tram(9, 14, -1), Tram(10, 11, -1), 
            Tram(11, 9, -1), Tram(12, 7, -1), Tram(13, 5, -1), Tram(14, 3, -1), Tram(15, 1, -1)
        ]
        self.create_timetables()

    def is_peak_hour(self, time):
        return (time.hour == 7 and time.minute >= 0) or \
               (time.hour == 8 and time.minute < 30) or \
               (time.hour >= 15 and time.hour < 18)

    def create_timetables(self):
        start_time = datetime(2024, 1, 1, 7, 0)  # Using a dummy date
        end_time = datetime(2024, 1, 1, 19, 0)

        for tram in self.trams:
            current_time = start_time

            while current_time < end_time:
                interval = timedelta(minutes=7.5 if self.is_peak_hour(current_time) else 15)
                tram.add_stop(current_time, self.stations[tram.current_station_index].name)
                current_time += interval
                tram.current_station_index += tram.direction

                if tram.current_station_index == len(self.stations):
                    tram.current_station_index = len(self.stations) - 2
                    tram.direction = -1
                elif tram.current_station_index == -1:
                    tram.current_station_index = 1
                    tram.direction = 1

    def print_tram_timetables(self):
        for tram in self.trams:
            print("#########")
            print(f"tram {tram.id}")
            for time, station in tram.timetable:
                print(f"{time.strftime('%H:%M')} - {station}")
            print("#########")

# Create the tram system
system = TramSystem()

# Print timetable for all trams
system.print_tram_timetables()
