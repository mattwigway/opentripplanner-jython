from opentripplanner import Graph
from PointSet import PointSet
from org.opentripplanner.routing.algorithm import EarliestArrivalSPTService
from org.opentripplanner.analyst import TimeSurface

class BatchProcessor:
    """
    Handles all of the specifics of marshalling data through the batch processor.
    """

    def __init__(self, graph=None, origins=None, destinations=None, routingRequest=None, cutoffMinutes=120):
        if graph is not None:
            self.setGraph(graph)
        
        if origins is not None:
            self.setOrigins(origins)

        if destinations is not None:
            self.setDestinations(destinations)

        if routingRequest is not None:
            self.setRoutingRequest(routingRequest)

        self.cutoffMinutes = cutoffMinutes

    def setOrigins(self, origins):
        'Set the origins for this batch analysis request'
        if isinstance(origins, str):
            self._origins = PointSet(origins)
        else:
            self._origins = origins

    def setDestinations(self, destinations):
        'Set the destinations for this batch analysis request'
        if isinstance(destinations, str):
            self._destinations = PointSet(destinations)
        else:
            self._destinations = destinations

    def setGraph(self, graph):
        if isinstance(graph, str):
            self._graph = Graph(graph)
        else:
            self._graph = graph

    def setRoutingRequest(self, routingRequest):
        self._routingRequest = routingRequest

    def run (self):
        """
        Run this batch request. It's perfectly safe to re-run this after tweaking some parameters; indeed, this is the
        recommended way to run many batch requests.
        Returns: a giant matrix with of travel times, in seconds, with origins on the rows and destinations on the columns
        """

        # Create a matrix to hold results
        # Silly python, no rep() function
        results = [None for i in xrange(len(self._origins))]

        # create an spt service
        sptService = EarliestArrivalSPTService()
        sptService.maxDuration = self.cutoffMinutes * 60

        # Create a sample set for the destinations
        destSamples = self._destinations._pointSet.getSampleSet(self._graph._graph)

        # TODO: threading
        # we use xrange here instead of range because xrange is a generator; there's no reason to create a list of
        # 10 million ints in RAM just to keep track of where we are
        oLen = len(self._origins)
        for origin in xrange(oLen):
            print 'Processing origin %s of %s' % (origin + 1, oLen)

            # build an SPT

            options = self._routingRequest.clone()
            # this is important
            options.batch = True
            options.setFrom(*self._origins[origin])
            options.setGraph(self._graph)

            spt = sptService.getShortestPathTree(options._routingRequest)
            tsurf = TimeSurface(spt)
            dtimes = destSamples.eval(tsurf)

            results[origin] = dtimes

        return results
            
            
