import sys

# Distance between single element clusters
def single_dist(u,v):
    if len(u) == 1 and len(v) == 1:
        return abs(  u[0] - v[0]  )


# Distances between clusters, provided you already know the distances of the clusters in previous states.
# Does not use recusion, instead it uses a list with information about distances of previously existing clusters
def d(s,t,v, distances):
    len_s = len(s)
    len_t = len(t)
    len_v = len(v)

    if method == "single":
        alpha_i = 0.5
        alpha_j = 0.5
        beta = 0
        gamma = -0.5
    elif method =="complete":
        alpha_i = 0.5
        alpha_j = 0.5
        beta = 0
        gamma = 0.5
    elif method == "average":
        alpha_i = len_s / ( len_s + len_t )
        alpha_j = len_t / ( len_s + len_t )
        beta = 0
        gamma = 0
    elif method == "ward":
        alpha_i = ( len_s + len_v ) / ( len_s + len_t + len_v )
        alpha_j = ( len_t + len_v ) / ( len_s + len_t + len_v )
        beta = -1 * ( len_v / ( len_s + len_t + len_v ) )
        gamma = 0

    # d(s,v)
    # if it exists, get distances[(s,v)], otherwise try distances[(v,s)].
    # If they both don't exist, then s = v and the distance between them is 0.
    distance_s_v = distances.get((s, v), distances.get((v, s), 0 ))
    # d(t,v)
    distance_t_v = distances.get((t, v), distances.get((v, t), 0 ))
    # d(s,t)
    distance_s_t = distances.get((s, t), distances.get((t, s), 0 ))
    
    distance_u_v = alpha_i * distance_s_v + alpha_j * distance_t_v + beta * distance_s_t + gamma * abs( distance_s_v - distance_t_v )
    return distance_u_v



# raise exception if we are given wrong parameters
if (args_count := len(sys.argv)) != 3:
    print(f"Two arguments expected, got {args_count - 1}")
    raise SystemExit(2)


method = sys.argv[1] # acts as global variable
file_name = sys.argv[2]


# getting the integer numbers from the file
f = open(file_name, 'r')
content = f.read().split(" ")
content = list(map(int , content))
content.sort()
f.close()


# creating the clusters as tuples in a list called clusters
clusters = [(i,) for i in content]


# gather all the initial distances between the clusters in a dictionary
# The dictionary distances contains all of the known distances between clusters that currently exist, but also clusters that existed in the past
distances = {}
for i in range(len(clusters)):
    for j in range(i + 1, len(clusters)):
        # the keys are tuples that contain the 2 clusters (which are also tuples)
        distances[ (clusters[i], clusters[j]) ] = single_dist(clusters[i], clusters[j])


# Go on with the clustering process, until only 1 cluster is left
while len(clusters) > 1:
    # Current distances is a dictionary containing the distances between the clusters, that are available to merge.
    current_distances = {}
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            current_distances[ (clusters[i], clusters[j]) ] = distances.get((clusters[i], clusters[j]), distances.get((clusters[j], clusters[i]), 0))

    # combine the 2 clusters with the minimum distance
    clusters_to_join = min(current_distances, key = current_distances.get)
    min_dist = current_distances[clusters_to_join]

    cluster_0 = clusters_to_join[0]
    cluster_1 = clusters_to_join[1]

    string_cluster_0 = ' '.join(list(map(str, cluster_0)))
    string_cluster_1 = ' '.join(list(map(str, cluster_1)))
    print( f"({string_cluster_0}) ({string_cluster_1}) {min_dist:.2f} {len(cluster_0) + len(cluster_1)}")

    #decide new distances after the 2 clusters join:
    for other_cluster in clusters:
        if other_cluster not in clusters_to_join:
            new_distance = d(cluster_0, cluster_1, other_cluster, distances)
            # append the new distance in the list with all the known distances
            distances[( cluster_0 + cluster_1, other_cluster )] = new_distance

    # replacing the previous 2 clusters, with the new one
    index_first = clusters.index(cluster_0)
    clusters[index_first] += clusters.pop(clusters.index(cluster_1))
    clusters[index_first] = tuple(sorted(clusters[index_first]))