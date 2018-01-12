"""Basic analytic tools for examining the distribution of degrees in graphs."""


from random import random, sample


def make_complete_dgraph(num_nodes):
    """
    (int) -> dict

    Return a dictionary corresponding to a complete directed graph
    (no self-loops) with the specified number of nodes, numbered 0
    to num_nodes-1 when num_nodes > 0. Otherwise, return a dictionary
    corresponding to the empty graph.
    """
    return {node: set(neighbor for neighbor in range(num_nodes)
            if neighbor != node) for node in range(num_nodes)}


def edge_count(dgraph):
    """
    (dict) -> int

    Return the number of edges of a graph.
    """
    return sum(len(neighbors) for neighbors in dgraph.values())


def make_er_dgraph(num_nodes, p):
    """
    (int, float) -> dict

    Return a dictionary corresponding to an Erdos-Renyi random, directed graph
    (no self-loops) with the specified number of nodes numbered 0 to
    num_nodes-1 when num_nodes > 0. Otherwise, return a dictionary
    corresponding to the empty graph. Edges have probability p of occurring.
    Use random.random.
    """
    graph = {}
    for node1 in range(num_nodes):
        graph[node1] = set([])
        for node2 in range(num_nodes):
            if random() < p and node2 != node1:
                graph[node1].add(node2)
    return graph


def compute_in_degrees(dgraph):
    """
    (dict) -> dict

    Return a dictionary with key-value pairs being (node, in-degree(node)).
    """
    in_degree_dict = {}
    for outgoing_edges in dgraph.values():
        for node in outgoing_edges:
            in_degree_dict[node] = in_degree_dict.get(node, 0) + 1
    return in_degree_dict


def in_degree_distribution(dgraph):
    """
    (dict) -> dict

    Compute the unnormalized distribution of the in-degrees of dgraph. Return
    a dictionary whose keys correspond to in-degrees of the nodes and whose
    values associated with each particular in-degree are the number of nodes
    with that in-degree. In-degrees with no corresponding nodes are not
    included.
    """
    in_degree_distr = {}
    in_degrees = compute_in_degrees(dgraph)
    for val in in_degrees.values():
        in_degree_distr[val] = in_degree_distr.get(val, 0) + 1
    return in_degree_distr


def normalize(dgraph):
    """
    (dict) -> dict

    Return the normalized in-degree distribution of dgraph.
    """
    unnormalized = in_degree_distribution(dgraph)
    num_edges = sum(unnormalized.values())
    return {key: (val / float(num_edges))
            for key, val in unnormalized.items()}


def dpa_algorithm(initial_size, end_size):
    """
    (int, int) -> dict

    Implement the Directed Preferential Attachment algorithm (DPA) returning
    a random directed graph. Edges are chosen iterively according to the
    proportion of previously-existing edges.
    """
    dpa_graph = make_complete_dgraph(initial_size)

    # store copies of node numbers as in-degrees to maintain the desired
    # probability of choosing a node: (indegree(node)+1)/(totalindegrees+|V|)
    node_numbers = [node for node in range(initial_size)
                    for _ in range(initial_size)]

    for new_node in range(initial_size, end_size):

        # compute a set of neighbors for new_node (outbound edges)
        # using the same maximum degree=initial_size during each iteration
        # use random.sample to select neighbors
        neighbors = set(sample(node_numbers, initial_size))

        # update the list of node numbers so that the probability as per the
        # formula is reflected in the number of instances of each node
        node_numbers.extend(list(neighbors))
        node_numbers.append(new_node)

        dpa_graph[new_node] = neighbors
    return dpa_graph
