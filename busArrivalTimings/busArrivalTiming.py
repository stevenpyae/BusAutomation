import requests
from bus_arrival import BusArrival

# Open the file for reading
with open('busData.txt', 'r') as file:
    lines = file.readlines()


def getaction():
    # insert the voice recognition here
    # Result should either be work or go out
    return "work"

action = getaction()

buses: list[BusArrival] = []

bus_search = BusArrival()

# Iterate through lines and create Person instances
for line in lines:
    parts = line.strip().split(',')  # Split the line into parts
    if parts[0] == action and len(parts) == 3:
            purpose, bus_code, bus_no = parts
            # Need a filter to separate work and dates
            bus_search = BusArrival(purpose, bus_code, bus_no)

url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode='

payload = {}
headers = {
    'AccountKey': 'uhAxrSlpRQCfSzBWImXBMA=='
}
# Get User's Input to find out where you are going.
# Filter buscode to match where you are going.
# Testing


response = requests.request("GET", url + bus_search.bus_code, headers=headers, data=payload)

filtered_response = response.text

dashboards = eval(response.content)

services_list = dashboards['Services']

for service in services_list:
    # If the service number matches the bus number + workBuscode
    if service['ServiceNo'] == bus_search.bus_no:
        print(f"Next Bus Arrival: {bus_search.bus_no}")
        # Convert to date time
        print(service['NextBus']['EstimatedArrival'].split('+')[0].replace('T', ' '))  # Clean up
        print(f"Second Bus Arrival: {bus_search.bus_no}")
        print(service['NextBus2']['EstimatedArrival'].split('+')[0].replace('T', ' '))  # Clean up

# Output in a UI/Text To speech to show what time the bus will be arriving
