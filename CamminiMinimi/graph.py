class Vertex:
    """
    The class representing a vertex.
    """

    def __init__(self, vertex_id):
        """
        The constructor of a new vertex object.

        :type vertex_id: str
        :param vertex_id: the id of the vertex
        """

        self.__id = vertex_id
        self.__adjacent = {}

    def __str__(self):
        """
        Returns the string representation of the vertex.

        :rtype: str
        :return: the string representation of the vertex
        """

        return str(self.__id) + ' adjacent: ' + str([x.__id for x in self.__adjacent])

    def add_neighbor(self, neighbor, weight=0):
        """
        Adds a new edge of the given weight between this vertex and the given one.
        By default the weight is equal to 0.

        :type neighbor: str
        :param neighbor: the id of the given vertex

        :type weight: float
        :param weight: the weight of the edge
        """

        self.__adjacent[neighbor] = weight

    def get_connections(self):
        """
        Gets all the adjacent vertices of the vertex.

        :rtype: dict_keys
        :return: all the ids of the adjacent nodes
        """

        return self.__adjacent.keys()

    def get_id(self):
        """
        Gets the id of the vertex.

        :rtype: str
        :return: the id of the vertex
        """

        return self.__id

    def get_weight(self, neighbor):
        """
        Gets the weight of the edge between this vertex and the given one.

        :type neighbor: str
        :param neighbor: the id of the given vertex

        :rtype: float
        :return: the weight of the edge
        """

        return self.__adjacent[neighbor]


class Graph:
    """
    The class representing a graph that consists of vertices and edges.
    """

    def __init__(self):
        """
        The constructor of a new graph object.
        """

        self.__vert_dict = {}
        self.__num_vertices = 0
        self.__weighted = 0

    def __iter__(self):
        """
        The iterator for the graph.

        :rtype: method
        :return: the iterator of the graph
        """

        return iter(self.__vert_dict.values())

    def __str__(self):
        """
        Returns the string representation of the graph.

        :rtype: str
        :return: the string representation of the graph
        """

        try:
            if self.__num_vertices == 0:
                raise EmptyGraphError
            graph = ""
            graph += "Graph:\n"
            for vs in self:
                graph += "Vertex" + " " + str(vs) + "\n"
                for vd in vs.get_connections():
                    vsid = vs.get_id()
                    vdid = vd.get_id()
                    if self.__weighted:
                        graph += "Arch: (%3s,%3s) Cost: %.4f\n" % (vsid, vdid, vs.get_weight(vd))
                    else:
                        graph += "Arch: (%3s,%3s)\n" % (vsid, vdid)
                    if vd is list(vs.get_connections())[-1] and vs is not list(self)[-1]:
                        graph += "\n"
            return graph.rstrip("\n")

        except EmptyGraphError:
            print("Error: The graph is not defined.")
            return ""

        except Exception:
            print("Error: The graph cannot be printed.")
            return ""

    def load_graph(self, filepath, weighted=0):
        """
        Loads the graph from the input txt file.
        By default the weighted is equal to 0 so the loaded graph is not weighted.

        :type filepath: str
        :param filepath: the location of the input file

        :type weighted: int
        :param weighted: the flag describing whether the graph is weighted (for all the non-zero values) or not (for 0)

        :rtype: int
        :return: the flag describing whether the graph has been loaded (1) or not (0)
        """

        self.__weighted = weighted

        num = 0
        try:
            fp = open(filepath, "r")
            line = fp.readline()

            while line:
                if line.split()[0] == "NODES":
                    # read the number of nodes
                    num = int(line.split()[1])

                if line.split()[0] == "ARCS":
                    line = fp.readline()

                    # read the edges
                    while line.split()[0] != "END":
                        arch = line.split()
                        vs = arch[0]
                        vd = arch[1]

                        # check whether the graph is weighted
                        if self.__weighted:
                            co = float(arch[2])

                        # ignore arches like (i, j) where i = j
                        if vs is not vd:
                            # check whether the graph is weighted
                            if self.__weighted:
                                self.add_edge(vs, vd, co)
                            else:
                                self.add_edge(vs, vd)

                        line = fp.readline()

                line = fp.readline()

            # check whether the number of nodes is correctly defined
            if num != self.__num_vertices:
                raise NumberOfNodesError

            return 1

        except IOError:
            self.__weighted = 0
            self.__num_vertices = 0
            self.__vert_dict = {}
            print("Error: The file does not appear to exist.")
            return 0

        except IndexError:
            self.__weighted = 0
            self.__num_vertices = 0
            self.__vert_dict = {}
            print("Error: The arches defined in the input file are probably incorrect.")
            return 0

        except NumberOfNodesError:
            self.__weighted = 0
            self.__num_vertices = 0
            self.__vert_dict = {}
            print("Error: The format of the input file is incorrect.")
            return 0

        except Exception:
            self.__weighted = 0
            self.__num_vertices = 0
            self.__vert_dict = {}
            print("Error: The input file cannot be read.")
            return 0

    def add_vertex(self, node):
        """
        Adds a new vertex to the graph.

        :type node: str
        :param node: the id of the vertex
        """

        try:
            if node not in self.__vert_dict:
                self.__num_vertices = self.__num_vertices + 1
                new_vertex = Vertex(node)
                self.__vert_dict[node] = new_vertex
            else:
                raise VertexIdError

        except VertexIdError:
            print("Error: The vertex with \"%s\" id already exists." % node)

        except Exception:
            print("Error: A new vertex cannot be added.")

    def add_edge(self, frm, to, cost=0):
        """
        Adds a new edge between the given vertices or updates it if the connection already exists.

        :type frm: str
        :param frm: the id of the first vertex

        :type to: str
        :param to: the id of the second vertex

        :type cost: float
        :param cost: the weight of the edge
        """

        if frm not in self.__vert_dict:
            self.add_vertex(frm)
        if to not in self.__vert_dict:
            self.add_vertex(to)

        try:
            self.__vert_dict[frm].add_neighbor(self.__vert_dict[to], cost)
            self.__vert_dict[to].add_neighbor(self.__vert_dict[frm], cost)

        except Exception:
            print("Error: A new edge cannot be added.")

    def get_vert_dict(self):
        """
        Gets the dictionary representation of the vertices of the graph.

        :rtype: dict
        :return: the dictionary representation of the vertices of the graph
        """

        return self.__vert_dict

    def get_num_vertices(self):
        """
        Gets the number of vertices.

        :rtype: int
        :return: the number of vertices
        """

        return self.__num_vertices

    def get_vertex(self, node):
        """
        Gets the vertex with the given id.

        :type node: str
        :param node: the id of the vertex

        :rtype: Vertex
        :return: the vertex with the given id
        """

        try:
            if node in self.__vert_dict:
                return self.__vert_dict[node]
            else:
                raise VertexIdError

        except VertexIdError:
            print("Error: The vertex with \"%s\" id does not exist." % node)
            return None

        except Exception:
            print("Error: The vertex cannot be returned.")
            return None

    def get_vertices(self):
        """
        Gets the ids of all the vertices of the graph.

        :rtype: dict_keys
        :return: the ids of all the vertices of the graph
        """

        return self.__vert_dict.keys()


class NumberOfNodesError(Exception):
    """ The number of nodes defined by the keyword "NODES" is not equal to the number of nodes existing in the input
    file. """

    def __init__(self):
        self.args = ("The number of nodes defined by the keyword \"NODES\" is not equal to the number of nodes "
                     "existing in the input file.",)


class EmptyGraphError(Exception):
    """ The graph is not defined. """

    def __init__(self):
        self.args = ("The graph is not defined.",)


class VertexIdError(Exception):
    """ The id of the vertex is incorrect. """

    def __init__(self):
        self.args = ("The id of the vertex is incorrect.",)


class LoadingError(Exception):
    """ The graph cannot be loaded. """

    def __init__(self):
        self.args = ("The graph cannot be loaded.",)
