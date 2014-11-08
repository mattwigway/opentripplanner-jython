from org.opentripplanner.analyst import PointSet as OtpPointSet
from PointFeature import PointFeature
from java.io import File

class PointSet:
    """
    Wraps an OTP Analyst PointSet
    """

    def __init__(self, infile=None, fmt=None, size=None):
        """
        Load a PointSet from the specified infile, with the specified format (default: auto-detect based on file extension)
        Formats available: csv shapefile
        """

        # no file: user will build pointset by hand
        if infile is None:
            if size is None:
                raise RuntimeError, "you must specify a size for an empty pointset"

            self._pointSet = OtpPointSet(size)

        else:
            # Autodetect format
            if fmt is None:
                if infile.lower().endswith('.csv'):
                    fmt = 'csv'
                elif infile.lower().endswith('.shp'):
                    fmt = 'shapefile'
                else:
                    raise ArgumentError, 'Unable to autodetect format for %s. Please specify a format manually' % infile

            fmt = fmt.lower()

            # load the pointset
            self._format = fmt

            if fmt == 'csv':
                self._pointSet = OtpPointSet.fromCsv(File(infile))

            elif fmt == 'shapefile' or fmt == 'shp':
                self._pointSet = OtpPointSet.fromShapefile(File(infile))

        # Make a place to store samples
        self._samples = dict()

    def link(self, graph):
        "Link points to the specified graph. This is used only for destinations; origins are linked automatically."

        graphId = graph.getId()

        # force re-link always, don't check if already linked
        self._samples[graphId] = self._pointSet.getSampleSet(graph._graph)

    def __setitem__(self, i, feat):
        self._pointSet.addFeature(feat._pointFeature, i)

    def __len__(self):
        return self._pointSet.featureCount()

    def __getitem__(self, i):
        return PointFeature(pointFeature=self._pointSet.getFeature(i))

    def __iter__ (self):
        # hacky way to make iteration work
        return (self[i] for i in xrange(len(self))).__iter__()
