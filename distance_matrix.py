import numpy as np
import requests
from sklearn.cluster import KMeans


input_data = [
    {"latitude": 52.5163, "longitude": 13.3777},
    {"latitude": 52.5200, "longitude": 13.4049},
    {"latitude": 52.5244, "longitude": 13.4050},
    {"latitude": 52.5186, "longitude": 13.3759},
    {"latitude": 52.5138, "longitude": 13.3928},
    {"latitude": 52.5206, "longitude": 13.2951},
    {"latitude": 52.5219, "longitude": 13.4132},
    {"latitude": 52.5034, "longitude": 13.4375},
    {"latitude": 52.5043, "longitude": 13.3325},
    {"latitude": 52.5336, "longitude": 13.3818}
]


origins = "|".join([f"{point['latitude']},{point['longitude']}" for point in input_data])
destinations = "|".join([f"{point['latitude']},{point['longitude']}" for point in input_data])

url = "https://maps.googleapis.com/maps/api/distancematrix/json"

params = {
    "origins": origins,
    "destinations": destinations,
    "key": "AIzaSyDk0hQ9zFdiD267NUC5WfGBYFaTtSrktj4"
}
response = requests.get(url, params=params)
api_result = response.json()


distance_matrix = []
for row in api_result['rows']:
    row_distances = [element['distance']['value'] for element in row['elements']]
    distance_matrix.append(row_distances)

print(distance_matrix)



distance_matrix = np.array([distance_matrix])

n_samples = distance_matrix.shape[0]
distance_matrix = distance_matrix.reshape(n_samples, -1)

k = 1

kmeans = KMeans(n_clusters=k, random_state=0).fit(distance_matrix)

cluster_labels = kmeans.labels_
print("Cluster labels:", cluster_labels)
















