from FlightRadar24 import FlightRadar24API
api = FlightRadar24API()

flights = api.get_flights(
    aircraft_type='PLF106'
)

print(flights)