# java imports

from org.opentripplanner.routing.impl import GraphServiceImpl

class GraphService:
    """
    Represents an OpenTripPlanner graphservice.
    Currently only supports disk-based graphs, but could be subclassed
    to support automated graph buiding
    """
    
    def __init__ (self, path):
        """
        path: the path to the graph
        """

        self.path = path
        self._graphService = GraphServiceImpl()
        self._graphService.setPath(self.path)
        self._graphService.startup()

    def getGraph (routerId = None):
        if routerId is not None:
            return self._graphService.getGraph(graph)

        else:
            return self._graphService.getGraph()
