from org.opentripplanner.analyst import PointSet as OtpPointSet
from java.io import File

class PointSet:
    """
    Wraps an OTP Analyst PointSet
    """

    def __init__(self, infile, fmt=None):
        """
        Load a PointSet from the specified infile, with the specified format (default: auto-detect based on file extension)
        Formats available: csv shapefile
        """

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


    def __len__(self):
        return self._pointSet.featureCount()

    def __getitem__(self, i):
        f = self._pointSet.getFeature(i)
        return (f.lat, f.lon)
