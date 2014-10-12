# wrap an opentripplanner pointfeature

class PointFeature:
    def __init__(self, pointFeature):
        self._pointFeature = pointFeature
        self.lat = pointFeature.lat
        self.lon = pointFeature.lon
        self.properties = pointFeature.properties
