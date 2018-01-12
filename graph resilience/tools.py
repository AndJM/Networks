"""
Tools for computing the resilience of an undirected graph including those for
computing its set of connected components and for determining the size of its
largest member.
"""


from random import random, shuffle, sample
from collections import deque


def make_complete_ugraph(num_nodes):
    """
    (int) -> dict

    Return a dictionary corresponding to a complete graph (no self-loops) with
    the specified number of nodes, numbered 0 to num_nodes - 1 when
    num_nodes > 0. Otherwise, return a dictionary corresponding to the empty
    graph.
    """
    return {node: set(neighbor for neighbor in range(num_nodes)
            if neighbor != node) for node in range(num_nodes)}


def copy_graph(ugraph):
    """Make a copy of a graph."""
    graph_copy = {}
    for node in ugraph:
        graph_copy[node] = set(ugraph[node])
    return graph_copy


def add_node(ugraph, node, neighbors):
    """
    (dict, int, set) -> None

    Add a node to an undirected graph with 0 or more existing adjacent nodes.
    """
    ugraph[node] = neighbors
    for neighbor in neighbors:
        ugraph[neighbor].add(node)


def delete_node(ugraph, node):
    """Delete a node from an undirected graph."""
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)


def edge_count(ugraph):
    """Returns the number of edges of a graph."""
    count = sum(len(ugraph[node]) for node in ugraph)
    return count / 2


def bfs_visited(ugraph, start_node):
    """
    (dict, int) -> set

    Return all nodes in ugraph visited by a breadth-first search starting at
    start_node.
    """
    myqueue = deque()
    myqueue.append(start_node)
    visited = deque()
    visited.append(start_node)
    while myqueue:
        node = myqueue.popleft()
        for neighbor in ugraph[node]:
            if neighbor not in visited:
                myqueue.append(neighbor)
                visited.append(neighbor)
    return set(visited)


def cc_visited(ugraph):
    """
    (dict) -> list

    Return a list of sets each consisting of all nodes in a connected
    component of ugraph.
    """
    nodes = set(ugraph.keys())
    components = []
    while nodes:
        start_node = nodes.pop()
        one_component = bfs_visited(ugraph, start_node)
        components.append(one_component)
        for node in one_component:
            nodes.discard(node)
    return components


def largest_cc_size(ugraph):
    """
    (dict) -> int

    Return the size of the largest connected component in ugraph.
    """
    components = cc_visited(ugraph)
    return len(max(components, key=len)) if components else 0


def compute_resilience(ugraph, attack_order):
    """
    (dict, list) -> list

    Return a list whose k+1th entry is the size of the largest connected
    component in the graph after the removal of the first k nodes in
    attack_order.

    For each node in the list, the function removes the given node and its
    edges from the graph and then computes the size of the largest connected
    component for the resulting graph. The first entry is the size of the
    largest connected component in ugraph.
    """
    graph = copy_graph(ugraph)
    ranking = [largest_cc_size(graph)]
    for node in attack_order:
        delete_node(graph, node)
        ranking.append(largest_cc_size(graph))
    return ranking


def random_order(ugraph):
    """
    (dict) -> list

    Return a list of the nodes in the graph in random order.
    Use random.shuffle.
    """
    nodes = list(ugraph.keys())
    shuffle(nodes)
    return nodes


def targeted_order(ugraph):
    """
    (dict) -> list

    Compute an attack sequence consisting of nodes of maximal degree,
    returning a list of nodes. Runs in quadratic time.
    """
    graph = copy_graph(ugraph)
    seq = []
    while graph:
        max_degree_node = max(graph, key=graph.get)
        seq.append(max_degree_node)
        delete_node(graph, max_degree_node)
    return seq


def fast_targeted_order(ugraph):
    """
    (dict) -> list

    Compute an attack sequence consisting of nodes of maximal degree,
    returning a list of nodes. Runs in linear time.
    """
    graph = copy_graph(ugraph)
    degree_sets = [set([]) for k in range(len(graph))]
    for node in graph:
        node_degree = len(graph[node])
        degree_sets[node_degree].add(node)
    seq = []
    for degree in reversed(range(len(degree_sets))):
        nodes = degree_sets[degree]
        while nodes:
            pop_node = nodes.pop()
            for neighbor in graph[pop_node]:
                degree_pop_node = len(graph[neighbor])
                degree_sets[degree_pop_node].remove(neighbor)
                degree_sets[degree_pop_node-1].add(neighbor)
            seq.append(pop_node)
            delete_node(graph, pop_node)
    return seq


def make_er_ugraph(num_nodes, p):
    """
    (int, float) -> dict

    Return a dictionary corresponding to an Erdos-Renyi random, undirected
    graph (no self-loops) with the specified number of nodes numbered 0 to
    num_nodes-1 when num_nodes > 0. Otherwise, return a dictionary
    corresponding to the empty graph. Edges have probability p of occurring.
    Use random.random.
    """
    graph = {node: set([]) for node in range(num_nodes)}
    for node1 in range(num_nodes):
        for node2 in range(node1+1, num_nodes):
            if random() < p:
                graph[node1].add(node2)
                graph[node2].add(node1)
    return graph


def upa_algorithm(initial_size, end_size):
    """
    (int, int) -> dict

    Implement the Undirected Preferential Attachment algorithm (UPA) returning
    a random undirected graph. Edges are chosen iterively according to the
    proportion of previously-existing edges.
    """
    upa_graph = make_complete_ugraph(initial_size)

    # store copies of node numbers as degrees to maintain the desired
    # probability of choosing a node: (indegree(node)+1)/(totalindegrees+|V|)
    node_numbers = [node for node in range(initial_size)
                    for _ in range(initial_size)]

    _add_node = add_node
    for new_node in range(initial_size, end_size):

        # compute a set of adjacent nodes (neighbors) for new_node using the
        # same degree=initial_size during each iteration
        # use random.sample to select neighbors
        neighbors = set(sample(node_numbers, initial_size))

        # update the list of node numbers so that the probability as per the
        # formula is reflected in the number of instances of each node
        node_numbers.extend(list(neighbors))
        node_numbers.append(new_node)

        _add_node(upa_graph, new_node, neighbors)

    return upa_graph
