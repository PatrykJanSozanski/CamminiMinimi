import sys

from graph import Graph, LoadingError
from spf import SPF


def ask_file_path():
    """
    Reads the filepath of the input file given by the user to the console.

    :rtype: str
    :return: the path of the input file given by the user
    """

    try:
        return input("Insert the name of the input file (with its location): ")

    except Exception:
        print("Error: The name of the input file cannot be read.")
        sys.exit(0)


def prepare_graph(graph, filepath):
    """
    Manages the loading of the graph from the input file.

    :type graph: Graph
    :param graph: the graph to be loaded with data form the input file

    :type filepath: str
    :param filepath: the path of the input file given by the user
    """

    try:
        if not graph.load_graph(filepath, 1):
            raise LoadingError

    except LoadingError:
        print("Endpoint: The graph from the file \"%s\" cannot be loaded." % filepath)
        sys.exit(0)

    except Exception:
        print("Endpoint: The graph cannot be loaded.")
        sys.exit(0)


def ask_source_node(graph):
    """
    Reads the id of the source node given by the user to the console.

    :type graph: Graph
    :param graph: the graph containing the source node

    :rtype: str
    :return: the id of the source node given by the user
    """

    again = 0
    read_node = ""

    while read_node not in graph.get_vertices():
        if not again:
            try:
                read_node = input("Insert the id of the source node: ")

            except Exception:
                print("Error: The id of the source node cannot be read.")

        elif again <= 3:
            try:
                print("Error: The \"%s\" node is not a part of the graph." % read_node)
                print("Nodes: " + str(list(graph.get_vertices())))
                read_node = input("Choose the id of the source node from the list shown above: ")

            except Exception:
                print("Error: The id of the source node cannot be read.")

        else:
            print("Endpoint: The id of the source node cannot be read.")
            sys.exit(0)

        again = again + 1

    return read_node


def print_graph(graph):
    """
    Prints the graph's string representation to console.

    :type graph: Graph
    :param graph: the graph to be printed
    """

    try:
        print("\n# The loaded graph's structure:\n")
        print(str(graph) + "\n")

    except Exception:
        print("Endpoint: The graph cannot be printed.")
        sys.exit(0)


def print_paths(spf):
    """
    Prints all the minimal paths to console.

    :type spf: SPF
    :param spf: the SPF object
    """

    try:
        print("\n# The found minimal paths:\n")
        print(str(spf.get_paths()) + "\n")

    except Exception:
        print("Endpoint: The minimal paths cannot be printed.")
        sys.exit(0)


def runner():
    """
    The entry point of the program.
    """

    print("###\n\n# Dijkstra's Shortest Path First (SPF) Algorithm\n")
    g = Graph()
    input_file = ask_file_path()
    prepare_graph(g, input_file)
    print_graph(g)
    source_node = ask_source_node(g)
    d = SPF(g, source_node)
    d.minimal_paths()
    print_paths(d)
    print("###")
