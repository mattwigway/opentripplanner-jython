from threading import Thread, Lock
from time import sleep

from org.opentripplanner.routing.algorithm import EarliestArrivalSPTService
from org.opentripplanner.analyst import TimeSurface

from opentripplanner import Graph
from PointSet import PointSet
from Matrix import Matrix

class BatchProcessor:
    """
    Handles all of the specifics of marshalling data through the batch processor.
    """

    def __init__(self, graph=None, origins=None, routingRequest=None, profileRequest=None,
            cutoffMinutes=120, threads=4):
        if graph is not None:
            self.setGraph(graph)

        if origins is not None:
            self.setOrigins(origins)

        if routingRequest is not None:
            self.setRoutingRequest(routingRequest)

        if profileRequest is not None:
            self.setProfileRequest(profileRequest)

        self.cutoffMinutes = cutoffMinutes
        self.threads = threads

    def setOrigins(self, origins):
        'Set the origins for this batch analysis request'
        if isinstance(origins, str):
            self._origins = PointSet(origins)
        else:
            self._origins = origins

    def getOrigins(self):
        return self._origins

    def setDestinations(self, destinations):
        'Set the destinations for this batch analysis request'


    def getDestinations(self):
        return self._destinations

    def setGraph(self, graph):
        if isinstance(graph, str):
            self._graph = Graph(graph)
        else:
            self._graph = graph

    def setRoutingRequest(self, routingRequest):
        self._routingRequest = routingRequest

    def setProfileRequest(self, profileRequest):
        self._profileRequest = profileRequest

    def run (self):
        """
        Run this batch request. It's perfectly safe to re-run this after tweaking some parameters; indeed, this is the
        recommended way to run many batch requests.
        This does not return anything. To get results, see eval. The reason for making separate functions is that you
        can analyze different sets of destinations without repeating the graph search.
        """

        # Create a matrix to hold results
        # Silly python, no rep() function
        self.results = [None for i in xrange(len(self._origins))]

        # TODO: threading
        # we use xrange here instead of range because xrange is a generator; there's no reason to create a list of
        # 10 million ints in RAM just to keep track of where we are
        oLen = len(self._origins)
        nextOrigin = xrange(oLen).__iter__()

        startLock = Lock()
        outputLock = Lock()

        def processOrigins(nextOrigin, results, routingRequest, graph, origins, oLen, startLock, outputLock):
            # create an spt service
            sptService = EarliestArrivalSPTService()
            sptService.maxDuration = self.cutoffMinutes * 60

            while True:
                startLock.acquire()

                try:
                    origin = nextOrigin.next()
                except StopIteration:
                    startLock.release()
                    return

                print 'Processing origin %s of %s' % (origin + 1, oLen)

                # build an SPT

                options = routingRequest.clone()
                # this is important
                options.batch = True
                orig = origins[origin]
                options.setFrom(orig.getLat(), orig.getLon())
                options.setGraph(graph)

                # now we should not need a lock anymore
                startLock.release()

                spt = sptService.getShortestPathTree(options._routingRequest)
                tsurf = TimeSurface(spt)

                outputLock.acquire()
                results[origin] = tsurf
                outputLock.release()

        # start as many threads as we want
        threads = [Thread(target=processOrigins, args=(nextOrigin, self.results, self._routingRequest, self._graph, self._origins, oLen, startLock, outputLock))
                   for i in range(self.threads)]

        for thread in threads:
            thread.run()

        # poll
        # TODO: don't poll
        while True:
            if all([not thread.isAlive() for thread in threads]):
                break

            sleep(10)


    def eval(self, destinations):
        '''Produce a travel time matrix from the origins to all destinations'''
        if isinstance(destinations, str):
            destinations = PointSet(destinations)

        mat = Matrix(len(self._origins), len(destinations))

        graphId = self._graph.getId()

        if not destinations._samples.has_key(graphId):
            destinations.link(self._graph)

        destSamples = destinations._samples[graphId]

        for i in xrange(len(self._origins)):
            mat.setRow(i, destSamples.eval(self.results[i]))

        return mat
