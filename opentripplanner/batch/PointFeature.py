# wrap an opentripplanner pointfeature

import org.opentripplanner.analyst.PointFeature as OtpPointFeature

class PointFeature:
    def __init__(self, id=None, lat=None, lon=None, pointFeature=None, **kwargs):
        if pointFeature is not None:
            self._pointFeature = pointFeature

        else:
            self._pointFeature = OtpPointFeature(id)
            self.setLat(lat)
            self.setLon(lon)
            for k, v in kwargs.iteritems():
                self[k] = v

    def setLat(self, lat):
        self._pointFeature.lat = lat

    def setLon(self, lon):
        self._pointFeature.lon = lon

    def getLat(self):
        return self._pointFeature.lat

    def getLon(self):
        return self._pointFeature.lon

    def getId(self):
        return self._pointFeature.id

    def __getitem__(self, key):
        "Get a named property; note that this must be an integer"
        return self._pointFeature.properties[key]

    def __setitem__(self, key, val):
        self._pointFeature.addAttribute(key, val)
