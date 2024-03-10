This repository provides sample code on KNN clustering based on physical distance between longitude and latitude coordinate points.

**Scenario**

Say we have a set of addresses on a map, which indicate at least one person living there.

**Assumptions**

For this example code, we assume to have the geolocation coordinates of each address. If not, it is possible to obtain those via the Google Maps Geolocation API.
We additionally assume that we have some kind of indicator attached to each point (geolocation) that shows how many people live at this point. For the example code, this is set to a mean of 2 within the example coordinates.

**Aim**

We want to be able to visit each point within a group once. Hereby, we aim to adhere to a maximum amount of people per point, as well as a maximum amount of distance travelled to visit each point once. Additionally, we set a maximum number of points per group to be respected.

**Approach**

I combine information from the following to reach the (tentative) aim:
1. Google Maps Distance Matrix API
    I use this API to calcuate the pairwise-distances between each point from the input coordinates. If I put 10 coordoinates, I expect a 10x10 square Matrix as result, with one row of 0s, the distance to itself.
2. Google Maps Route API
    This API is called to get the an overview of distance travelled (by car) for each cluster. It is the goal to specify a limit of how much doistance should be allowed to be covered for each group.
3. KNN Clustering Algorithm
    Last but not least, I apply simple KNN clustering, based on physical distances of each point (given by the Distance Matrix), instead of common Euclidian Distance. Then, I cluster group mmebership for each point, gives a dynamic number of k (number of clusters).
