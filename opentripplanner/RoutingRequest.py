from org.opentripplanner.routing.core import TraverseModeSet, RoutingRequest as OtpRoutingRequest
from org.opentripplanner.common.model import GenericLocation

class RoutingRequest:
    'Wraps an OpenTripPlanner RoutingRequest'

    def __init__ (self, routingRequest = None):
        if routingRequest is None:
            self.__dict__['_routingRequest'] = OtpRoutingRequest()
        else:
            self.__dict__['_routingRequest'] = routingRequest

    # Since RoutingRequests have a ton of attributes, we don't attempt to wrap them all
    # this also means that if OTP gets more RoutingRequest attributes (not unheard of by a long shot)
    # it will automatically be accessible
    def __setattr__ (self, name, value):
        setattr(self._routingRequest, name, value)

    def __getattr__(self, name):
        return getattr(self._routingRequest, name)

    def clone (self):
        return RoutingRequest(self._routingRequest.clone())

    def setGraph (self, graph):
        self._routingRequest.setRoutingContext(graph._graph)

    def setFrom (self, lat, lon):
        setattr(self._routingRequest, 'from', GenericLocation(lat, lon))

    def setModes(self, modes):
        self._routingRequest.setModes(TraverseModeSet(modes))
