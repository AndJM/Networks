"""This module contains data loading and visualization functionality."""


# import urllib2
import matplotlib.pyplot as plt
from tools import *

FILENAME = 'alg_phys-cite.txt'
URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"


def info(graph, name='Graph'):
    """Print node and edge counts"""
    count_nodes = len(graph)
    count_edges = edge_count(graph)
    print("Created directed graph {0} with {1} nodes and {2} edges".format(
                                            name, count_nodes, count_edges))


def load_graph():
    """Load a graph from file and return a dictionary representation."""
    graph = {}

    def process_lines(datafile):
        for line in datafile:
            if not line.startswith(' '):  # actual file ends with an empty line
                line = line.strip()
                line = line.split(' ')
                yield line

    # graph_file = urllib2.urlopen(URL)
    with open(FILENAME) as graph_file:
        for line in process_lines(graph_file):
            node = int(line[0])
            graph[node] = set([])
            for neighbor in line[1:]:
                graph[node].add(int(neighbor))
    return graph


def make_plots():
    """Create loglog scatter plots of the distributions."""

    citation_graph = load_graph()
    info(citation_graph, "'Citation'")
    citation_graph_norm = normalize(citation_graph)
    make_points = [(key, val) for key, val in citation_graph_norm.items()]
    xvals, yvals = zip(*make_points)
    plt.loglog(xvals, yvals, '.')
    plt.title('In-degree distribution of alg_phys-cite')
    plt.xlabel('Log(In-Degree)')
    plt.ylabel('log(Normalized Frequency)')
    plt.show()

    # values for num_nodes and prob are sufficient in showing an ER graph is
    # not a good model for the citation graph
    num_nodes = 10000
    prob = 0.1
    er_graph = make_er_dgraph(num_nodes, prob)
    info(er_graph, "'ER'")
    er_plot_norm = normalize(er_graph)
    make_points = [(key, val) for key, val in er_plot_norm.items()]
    xvals, yvals = zip(*make_points)
    plt.loglog(xvals, yvals, '.')
    plt.title('In-degree distribution of ER graph '
              'for n={0} and p={1}'.format(num_nodes, prob))
    plt.xlabel('Log(In-Degree)')
    plt.ylabel('Log(Normalized Fequency)')
    plt.show()

    # values that yield a DPA graph roughly the same in nodes and edges as
    # the citation graph
    initial_size = 12
    end_size = 27770
    dpa_graph = dpa_algorithm(initial_size, end_size)
    info(dpa_graph, "'DPA'")
    dpa_plot_norm = normalize(dpa_graph)
    make_points = [(key, val) for key, val in dpa_plot_norm.items()]
    xvals, yvals = zip(*make_points)
    plt.loglog(xvals, yvals, '.')
    plt.title('In-degree distribution of DPA graph '
              'for m={0} and n={1}'.format(initial_size, end_size))
    plt.xlabel('Log(In-degree)')
    plt.ylabel('Log(Normalized Fequency)')
    plt.show()


if __name__ == '__main__':
    make_plots()
    exit()
