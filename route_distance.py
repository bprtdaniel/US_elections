import numpy as np
import requests


# Define the coordinates
destinations = [
    {"latitude": 52.5163, "longitude": 13.3777},
    {"latitude": 52.5186, "longitude": 13.3767},
    {"latitude": 52.5098, "longitude": 13.3759},
    {"latitude": 52.5138, "longitude": 13.3928},
    {"latitude": 52.5194, "longitude": 13.4009},
    {"latitude": 52.5161, "longitude": 13.4026},
    {"latitude": 52.5219, "longitude": 13.4132},
    {"latitude": 52.5225, "longitude": 13.4023},
    {"latitude": 52.5075, "longitude": 13.3903}
]

origins = [
    {"latitude": 52.5206, "longitude": 13.2951}
]

# Extract start and end coordinates
start = origins[0]
end = destinations[0]

# Extract waypoints
waypoints = destinations[1:]

# Construct the request payload
payload = {
    "origin": f"{start['latitude']},{start['longitude']}",
    "destination": f"{end['latitude']},{end['longitude']}",
    "waypoints": "|".join([f"{wp['latitude']},{wp['longitude']}" for wp in waypoints]),
    "mode": "driving",
    "key": "AIzaSyDk0hQ9zFdiD267NUC5WfGBYFaTtSrktj4"
}

# Define the API endpoint
url = 'https://maps.googleapis.com/maps/api/directions/json'

# Make the GET request
response = requests.get(url, params=payload)

# Print the response
print(response.json())

api_result = response.json()


def calculate_total_distance(api_result):
    total_distance = 0
    for route in api_result['routes']:
        for leg in route['legs']:
            total_distance += leg['distance']['value']
    return total_distance

# Example usage:
api_result = api_result  # Your API result here
total_distance = calculate_total_distance(api_result)
print(f"Total distance: {total_distance} meters")