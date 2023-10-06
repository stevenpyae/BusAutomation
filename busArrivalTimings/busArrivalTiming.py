from typing import List
import requests
from datetime import datetime
from bus_arrival import BusArrival
import speech_input as si


# Open the file for reading
def read_bus_data(file_path='busData.txt') -> List[str]:
    with open(file_path, 'r') as file:
        return file.readlines()


def make_api_request(bus_code, headers):
    url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode='
    response = requests.get(url + bus_code, headers=headers)
    response.raise_for_status()  # Raise an exception for bad responses
    return eval(response.content)


def get_bus_data(action):
    lines = read_bus_data()

    bus_search = BusArrival()

    for line in lines:
        parts = line.strip().split(',')
        if parts[0] == action and len(parts) == 3:
            purpose, bus_code, bus_no = parts
            bus_search = BusArrival(purpose, bus_code, bus_no)

    headers = {'AccountKey': 'uhAxrSlpRQCfSzBWImXBMA=='}

    try:
        dashboards = make_api_request(bus_search.bus_code, headers)['Services']

        for service in dashboards:
            if service['ServiceNo'] == bus_search.bus_no:
                print(f"Next Bus Arrival: {bus_search.bus_no}")
                print(datetime.strptime(service['NextBus']['EstimatedArrival'].split('+')[0], '%Y-%m-%dT%H:%M:%S'))
                print(f"Second Bus Arrival: {bus_search.bus_no}")
                print(datetime.strptime(service['NextBus2']['EstimatedArrival'].split('+')[0], '%Y-%m-%dT%H:%M:%S'))
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error processing API response: {e}")

def main():
    while True:
        command = si.listen()

        if command:
            print(f"You said: {command}")
            si.speak("You said: " + command)

            # Add your logic to handle different commands here

            if command == "stop":
                break


if __name__ == "__main__":
    main()