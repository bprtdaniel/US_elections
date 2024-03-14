# Work-in-progress script that aims to create independent functions to (1) create distance matrix (2) construct kneans clusters (3) run all three checks on distance, maximum points, maximum number of people.
# Create one overall function that incoporates all steps and checks, then updates k in case any of the maximum thresholds are broken.
# Update k and rerun function until k is large enough to meet thresholds.

import numpy as np
import requests
from sklearn.cluster import KMeans


lat_long = input_data = [
    {"latitude": 52.5163, "longitude": 13.3777, "people": 1},
    {"latitude": 52.5200, "longitude": 13.4049, "people": 3},
    {"latitude": 52.5244, "longitude": 13.4050, "people": 2},
    {"latitude": 52.5186, "longitude": 13.3759, "people": 2},
    {"latitude": 52.5138, "longitude": 13.3928, "people": 1},
    {"latitude": 52.5206, "longitude": 13.2951, "people": 3},
    {"latitude": 52.5219, "longitude": 13.4132, "people": 2},
    {"latitude": 52.5034, "longitude": 13.4375, "people": 1},
    {"latitude": 52.5043, "longitude": 13.3325, "people": 2},
    {"latitude": 52.5336, "longitude": 13.3818, "people": 3}
]



# Initaitve best guess global k number of clusters k
k = 2



def get_matrix(input_data, api_key):
    
    #Define origin, destination and key parameters for API request
    
    origins = "|".join([f"{point['latitude']},{point['longitude']}" for point in input_data])
    destinations = "|".join([f"{point['latitude']},{point['longitude']}" for point in input_data])
    api_key = "INSERT_KEY"
    url_matrix = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    # Define parameters
    params = {
        "origins": origins,
        "destinations": destinations,
        "key": api_key
    }
    # Call API
    response = requests.get(url_matrix, params=params)
    api_result_matrix = response.json()
    
    # Construct Matrix
    distance_matrix = []
    for row in api_result_matrix['rows']:
        row_distances = [element['distance']['value'] for element in row['elements']]
        distance_matrix.append(row_distances)

    distance_matrix = np.array(distance_matrix)
    
    return distance_matrix


def clustering(distance_matrix, k):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(distance_matrix)
    
    cluster_labels = kmeans.labels_
    
    return cluster_labels


def check_nop(cluster_labels, max_amount_of_people):
    
    clusters = [[] for _ in range(len(set(cluster_labels)))]
    for i, point in enumerate(input_data):
        clusters[cluster_labels[i]].append(point)

    # Filter out clusters that exceed the maximum amount of people, return the filtered clusters
    filtered_clusters = []
    for cluster in clusters:
        # Access each point within a cluster and sum its people value
        people_count = sum(point['people'] for point in cluster)
        # Print error message if sum people value is above the maximum amount of people per cluster
        # Otherwise, append the cluster to the filtered clusters list
        if people_count > max_amount_of_people:
            print(f"Cluster with {people_count} people exceeds the maximum of {max_amount_of_people}")
        else:
            filtered_clusters.append(cluster)
    return filtered_clusters


"""
def check_num_points(filtered_clusters, k):
    
    # Get list of filtered clusters that passed NOP check and check for max num points in cluster k
    
    clusters_post_nop = [[] for _ in range(len(set(filtered_clusters)))]
    for i, point in enumerate(filtered_clusters):
        clusters_post_nop[filtered_clusters[i]].append(point)
"""
    


def check_distance_travelled(filtered_clusters, api_key, max_route_distance):
    
    valid_clusters = []
    
    
    for cluster, _ in filtered_clusters:
        # For the Google Maps Route API, we need to specify the origin, destination and waypoints
        waypoints = "|".join([f"{point['latitude']},{point['longitude']}" for point in cluster])
        origin = f"{cluster[0]['latitude']},{cluster[0]['longitude']}"
        destination = f"{cluster[-1]['latitude']},{cluster[-1]['longitude']}"
        # Set the url for this API, define the parameters and call the API, save the result
        url_route = "https://maps.googleapis.com/maps/api/directions/json"
        params_route = {
            "origin": origin,
            "destination": destination,
            "waypoints": waypoints,
            "key": api_key
        }
        response = requests.get(url_route, params=params_route)
        data = response.json()
        
        # Initiate the total distance as 0, and iterate through the routes and legs to sum the distances. "Legs" are given by the API result as the distance betweene two waypoints.
        # To get the full distance of the route, we need to sum the distances of all legs.
        total_distance = 0
        for route in data['routes']:
            for leg in route['legs']:
                total_distance += leg['distance']['value']
        
        # Print an error message if the total distance exceeds the maximum distance threshold, otherwise append the cluster to the filtered clusters list
        if total_distance > max_route_distance * 1000:
            print(f'Cluster with {total_distance} meters exceeds the maximum of {max_distance_threshold} meters')
        else:
            valid_clusters.append(cluster)
    return valid_clusters



def overall_loop(input_data, api_key, k, max_amount_points, max_amount_of_people, max_route_distance):
    while True:
        distance_matrix = get_matrix(input_data, api_key)
        k_clusters = clustering(distance_matrix, k)
        filtered_clusters = check_nop(k_clusters, max_amount_of_people)
        
        # Introduce max point check for filtered clustes that passed max nop
        
        if filtered_clusters:
            filtered_clusters_nop = check_distance_travelled(filtered_clusters, api_key, max_route_distance)
            if not filtered_clusters_nop:
                print(f'Clusters have exceeded maximum distance travelled after passing nop check, increasing number of k')
                k += 1
            else:
                break
        else:
            print(f'Cluster result has exceeded nop, increasing number of k')
            k += 1
            
            

api_key = "INSERT_KEY"
overall_loop(lat_long, api_key, 3, 40, 20, 200)