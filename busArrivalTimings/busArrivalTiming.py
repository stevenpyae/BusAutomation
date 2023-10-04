from typing import List, Tuple

import requests
import re
from datetime import datetime


class BusArrival:
    purpose: str
    busCode: str
    busNo: str

    def __init__(self, purpose=None, bus_code=None, bus_no=None):
        self.purpose = purpose
        self.busCode = bus_code
        self.busNo = bus_no

    def input_bus_properties(self, purpose, bus_code, bus_no):
        self.purpose = purpose
        self.busCode = bus_code
        self.busNo = bus_no


# Open the file for reading
with open('busData.txt', 'r') as file:
    lines = file.readlines()


def getaction():
    # insert the voice recognition here
    # Result should either be work or go out
    return "work"


action = getaction()

buses: list[BusArrival] = []

bus_search: BusArrival = BusArrival()

# Iterate through lines and create Person instances
for line in lines:
    parts = line.strip().split(',')  # Split the line into parts
    if parts[0] == action:
        if len(parts) == 3:
            purpose, busCode, busNo = parts
            # Need a filter to separate work and dates
            bus_search.input_bus_properties(purpose, busCode, busNo)

url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode='

payload = {}
headers = {
    'AccountKey': 'uhAxrSlpRQCfSzBWImXBMA=='
}
# Get User's Input to find out where you are going.
# Filter buscode to match where you are going.
# Testing


response = requests.request("GET", url + bus_search.busCode, headers=headers, data=payload)

filtered_response = response.text

dashboards = eval(response.content)

services_list = dashboards['Services']

for service in services_list:
    # If the service number matches the bus number + workBuscode
    if service['ServiceNo'] == bus_search.busNo:
        print(f"Next Bus Arrival: {bus_search.busNo}")
        # Convert to date time
        print(service['NextBus']['EstimatedArrival'].split('+')[0].replace('T', ' '))  # Clean up
        print(f"Second Bus Arrival: {bus_search.busNo}")
        print(service['NextBus2']['EstimatedArrival'].split('+')[0].replace('T', ' '))  # Clean up

# Output in a UI/Text To speech to show what time the bus will be arriving
