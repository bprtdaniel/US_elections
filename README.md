# KNN Clustering for Geographic Data

This repository provides sample code on KNN clustering based on the physical distance between longitude and latitude coordinate points.

## Overview

The following code replaces the manual drawing of clusters, made up of a set number of individual points on a map.

## Scenario 

We have a set of addresses on a map, each representing the home address of at least one person to be visited. One point may represent the home address of several people.

## Assumptions

For this example code, we assume:

1. Geolocation coordinates of each address are available. If not, they can be obtained via the Google Maps Geolocation API.
2. Each point has an indicator showing how many people live at that location. In this example, we set this indicator to a mean of 2 within the provided coordinates.

## Aim

The goal is to visit each point within a group once, adhering to:

1. A maximum number of people per point.
2. A maximum distance traveled to visit each point once.
3. A maximum number of points per group.

## Approach

The approach combines information from:

1. Google Maps Distance Matrix API: Calculates pairwise distances between each point from the input coordinates. For 10 coordinates, a 10x10 square matrix is expected as a result, with one row of 0s representing the distance to itself.
2. Google Maps Route API: Provides an overview of the distance traveled (by car) for each cluster. This API also offers distance information for each leg of the route, as well as the total distance.
3. KNN Clustering Algorithm: Applies KNN clustering based on the physical distances of each point (from the Distance Matrix) instead of the common Euclidean Distance. This assigns cluster membership for each point, with a dynamic number of clusters.


## Notebooks Overview


- **cluster.ipynb**: This notebook contains a basic implementation of the clustering approach.
- **advanced_function.ipynb**: In this notebook, we apply the same logic as in the basic implementation. However, it includes an enhanced function that considers:
    - A maximum number of people allowed to visit within a defined cluster.
    - A maximum distance necessary to visit each point once.
- **advanced_script.py** establishes a work-in-progress function that aims to include (1) a check on the overall distance travelled and (2) a check of the amount of people in a cluster and continuously updates the number of clusters k in case the maximums are exceeded. The function should run until none of the thresholds are broken. Additionally, (3) a check of the number of overall points in a given cluster will also be included here/
 
## Next Steps
- A Google-Maps-based visualization for the KNN-produced cluster labels.
- Add a maximum number of geolocation points per cluster threshold into advanced_function.ipynb
- Add an automatic loop for the advanced_function to continuously update the number of clusters k, if thresholds are exceeded and more clusters need to be introduced to stay within the limit.
