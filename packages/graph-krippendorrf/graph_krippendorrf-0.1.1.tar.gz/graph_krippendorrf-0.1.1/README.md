# Krippendorrf-alpha-for-graph
a modification of Krippendorrf's alpha for graph, modified from this implementation (https://github.com/grrrr/krippendorff-alpha/blob/master/krippendorff_alpha.py)

### Graph Metrics
1. Normalized graph edit distance
    - normalized by computing distance between g1 and g0 and between g2 and g0
    - g0 is an empty graph

### Usage

`krippendorff_graph(data, metric=graph_edit_distance, missing_items=missing, convert_items=set, distance_matrix_path="./distance_matrix.json")`

distance_matrix_path caches graph distance matrix as json. Computing this distance matrix might take long. 