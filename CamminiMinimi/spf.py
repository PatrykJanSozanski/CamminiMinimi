import math


class SPF:
    """
    The class representing Dijkstra's Shortest Path First (SPF) algorithm.
    """

    def __init__(self, graph, source_node):
        """
        The constructor of a new SPF object.

        :type graph: Graph
        :param graph: the graph to be considered

        :type source_node: str
        :param source_node: the source node
        """

        try:
            self.__source_node = str(source_node)
            self.__graph = graph
            self.__correct = True
            self.__previous = {}
            self.__costs = {}

            if source_node not in graph.get_vertices():
                raise IncorrectParametersError

        except IncorrectParametersError:
            self.__correct = False
            print("Error: The \"%s\" node is not the part of the given graph." % self.__source_node)

        except Exception:
            self.__correct = False
            print("Error: The object cannot be created.")

    def minimal_paths(self):
        """
        Calculates the minimal paths from the source node to all the other nodes of the graph and saves the result in
        previous attribute and the costs attribute.
        """

        try:
            if self.__correct:
                # the set of the nodes to which the minimal path has not been found
                # at the beginning all the nodes are unmarked
                unmarked_nodes = set(self.__graph.get_vertices())
                # the dictionary that contains pairs like (n : c) where n is the id of the node and c is the cost to
                # reach the node n form the source node
                self.__costs = {}
                # the dictionary that contains pairs like (n : p) where n is the id of the node and p is the id of the
                # previous node on the minimal path from the source node to the n node
                self.__previous = {}

                for v in self.__graph.get_vertices():
                    # at the begging cost to all unmarked nodes is infinite
                    self.__costs[v] = math.inf
                    # at the begging no precedence relationship is defined
                    self.__previous[v] = None

                # by the convention the cost to reach the source node is equal to 0
                self.__costs[self.__source_node] = 0
                # by the convention the preceding node to the source node is the source node
                self.__previous[self.__source_node] = self.__source_node

                # do while the set of the unmarked nodes is not empty
                while len(unmarked_nodes) > 0:
                    # get the element with the lowest cost from among all the unmarked nodes
                    minimum = math.inf
                    minimum_node = None
                    for node in unmarked_nodes:
                        if self.__costs[node] < minimum:
                            minimum = self.__costs[node]
                            minimum_node = node
                    v = self.__graph.get_vert_dict().get(minimum_node)

                    # remove the element with the lowest cost
                    unmarked_nodes.remove(v.get_id())

                    # do for each arch originating form v
                    for w in v.get_connections():
                        # update the dictionaries if new minimal path has been found
                        if self.__costs[v.get_id()] + v.get_weight(w) < self.__costs[w.get_id()]:
                            self.__previous[w.get_id()] = v.get_id()
                            self.__costs[w.get_id()] = self.__costs[v.get_id()] + v.get_weight(w)

            else:
                raise IncorrectParametersError

        except IncorrectParametersError:
            print("Error: The minimal paths cannot be calculated due to incorrect algorithm's parameters.")

        except Exception:
            print("Error: The minimal paths cannot be calculated.")

    def get_cost(self, node):
        """
        Gets the cost of the minimal path from the source node to the given destination node.

        :type node: str
        :param node: the id of the destination node

        :rtype: float
        :return: the cost of the minimal path from the source node to the given node
        """

        try:
            if self.__costs == {}:
                raise UnknownCostError
            elif node not in self.__graph.get_vertices():
                raise IncorrectParametersError

            return self.__costs.get(node)

        except UnknownCostError:
            print("Error: The minimal paths has not been calculated.")
            return math.inf

        except IncorrectParametersError:
            print("Error: The \"%s\" node is not a part of the given graph." % node)
            return math.inf

        except Exception:
            print("Error: The cost to the node \"%s\" cannot be returned." % node)
            return math.inf

    def get_costs(self):
        """
        Gets the costs of all the possible minimal paths form the source node in the graph.

        :rtype: str
        :return: the costs of all the possible minimal paths form the source node
        """

        try:
            if self.__costs == {} or self.__previous == {}:
                raise UnknownCostError
            else:
                costs = "Costs:\n"
                for p in self.__graph.get_vertices():
                    costs = costs + "[" + self.__source_node + " -> " + p + "] Cost: " + str(self.get_cost(p)) + "\n"
                return costs.rstrip("\n")

        except UnknownCostError:
            print("Error: The minimal paths has not been calculated.")
            return ""

        except Exception:
            print("Error: The minimal costs cannot be returned.")
            return ""

    def get_path(self, node, iter=0):
        """
        Gets the minimal path form the source node to the given destination node.

        :type iter: int
        :param iter: the auxiliary variable for recursion

        :type node: str
        :param node: the id of the destination node

        :rtype: str
        :return: the minimal path from the source node to the given node
        """

        try:
            if self.__costs == {} or self.__previous == {}:
                raise UnknownCostError
            elif node not in self.__graph.get_vertices():
                raise IncorrectParametersError
            else:
                path = ""
                if iter == 0 and node == self.__source_node:
                    path = "Path: [%s] " % node + "Cost: " + str(self.get_cost(node))
                elif iter == 0 and node != self.__source_node:
                    path = self.get_path(self.__previous[node], iter + 1) + "%s] " % node + "Cost: " + str(self.get_cost(node))
                elif node == self.__source_node:
                    path = "Path: [%s -> " % node + path
                else:
                    path = self.get_path(self.__previous[node], iter + 1) + "%s -> " % node

                return path

        except UnknownCostError:
            print("Error: The minimal paths has not been calculated.")
            return ""

        except IncorrectParametersError:
            print("Error: The \"%s\" node is not a part of the given graph." % node)
            return ""

        except Exception:
            print("Error: The minimal path from the node \"%s\" to the node \"%s\" cannot be returned." % (self.__source_node, node))
            return ""

    def get_paths(self):
        """
        Gets all the possible minimal paths form the source node in the graph.

        :rtype: str
        :return: all the possible minimal paths form the source node
        """

        try:
            if self.__costs == {} or self.__previous == {}:
                raise UnknownCostError
            else:
                paths = "Paths:\n"
                for p in self.__graph.get_vertices():
                    paths = paths + self.get_path(p) + "\n"
                return paths.rstrip("\n")

        except UnknownCostError:
            print("Error: The minimal paths has not been calculated.")
            return ""

        except Exception:
            print("Error: The minimal paths cannot be returned.")
            return ""

    def set_graph(self, graph, source_node):
        """
        Changes the graph and the source node.

        :type graph: Graph
        :param graph: the new Graph object

        :type source_node: str
        :param source_node: the id of the new source node
        """

        try:
            if source_node not in graph.get_vertices():
                raise IncorrectParametersError
            else:
                self.__graph = graph
                self.__source_node = source_node
                self.__correct = True
                self.__previous = {}
                self.__costs = {}

        except IncorrectParametersError:
            self.__correct = False
            print("Error: The \"%s\" node is not the part of the given graph." % source_node)

        except Exception:
            print("Error: The graph cannot be changed.")

    def get_graph(self):
        """
        Gets the graph

        :rtype: Graph
        :return: the graph.
        """

        return self.__graph

    def set_source_node(self, source_node):
        """
        Changes the source node.

        :type source_node: str
        :param source_node: the id of the new source node
        """

        try:
            if source_node not in self.__graph.get_vertices():
                raise IncorrectParametersError
            else:
                self.__source_node = source_node
                self.__correct = True
                self.__previous = {}
                self.__costs = {}

        except IncorrectParametersError:
            print("Error: The \"%s\" node is not the part of the given graph." % source_node)

        except Exception:
            print("Error: The source node cannot be changed.")

    def get_source_node(self):
        """
        Gets the id of the source node.

        :rtype: str
        :return: the id of the source node
        """

        return self.__source_node


class UnknownCostError(Exception):
    """ The minimal paths has not been calculated. """

    def __init__(self):
        self.args = ("The minimal paths has not been calculated.",)


class IncorrectParametersError(Exception):
    """ The node is not the part of the graph. """

    def __init__(self):
        self.args = ("The node is not a part of the graph.",)
