import os.path
from GraphService import GraphService

class Graph:
    """Represents an OpenTripPlanner graph"""

    def __init__(self, graph):
        """
        Read the graph at the location specified by Graph.
        This function is also used internally to wrap an org.opentripplanner.routing.Graph, and
        can be called that way as well.
        """

        if isinstance(graph, str):
            # We need to load the graph from a file
            if not os.path.exists(graph):
                raise IOError, 'No such file or directory %s' % graph

            if os.path.isdir(graph):
                path = graph
                routerId = None

            else:
                # must be a file
                path = os.path.dirname(graph)
                routerId = os.path.basename(graph)

            self._graphService = GraphService(path)
            self._graph = self._graphService._getGraph(routerId)

        else:
            # We're wrapping a graph
            self._graph = graph
