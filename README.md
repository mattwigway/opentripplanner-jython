# OpenTripPlanner.py: OpenTripPlanner bindings for Python

This is a library to allow the use of the open-source [OpenTripPlanner](http://www.opentripplanner.org) journey planning engine from within Python (or, more specifically, Jython). The library is intended to allow low-level access to OTP internals from Python; if you just want to retrieve journey plans, you'd probably be better off spinning up an OTP instance directly, and then hitting its HTTP interface and processing the resultant XML or JSON.

The software currently provides bindings only for accessibility analysis capabilities, and not general journey planning. However, it is architected in such a way that it could be made more general in the future.

## Example

This finds the travel time to the closest high school from every block in Chicago (actually, to be pedantic, it finds the travel time from the closest high school to every block in the afternoon; there are technical limitiations that don't allow us to the former in an efficient matter, but these should be resolved soon).

First, you'll need to build a graph. Then, with your CLASSPATH environment variable set to the path of the OTP JAR, and your graph called `graph/Graph.obj` in the current directory, the following should work:

```python
#!/usr/bin/jython

from opentripplanner import RoutingRequest
from opentripplanner.batch import BatchProcessor

# Set the parameters for our search
r = RoutingRequest()
r.clampInitialWait = 1800 # 30 minutes
r.dateTime = 1412974800 # Friday, Oct. 10th, 2014, 4:00 pm CDT
# I think arriveBy doesn't work yet
r.setModes('WALK,TRANSIT')

# Create a BatchProcessor
b = BatchProcessor(
    # Where is Graph.obj?
    graph='graph',
    # What are the origins for the analysis?
    origins='highschools.shp',
    # What are the destinations?
    destinations='blocks.shp',
    # What are the parameters for the search?
    routingRequest=r,
    # This is for efficiency; we stop the algorithm running after it has found all blocks within a certain number of minutes of a school
    # every place in the city is surely within 60 minutes of a school
    cutoffMinutes=60,
    # I have four cores but eight hyperthreading cores, and that seemed
    # to count with the old Java batch analyst
    threads=8
)

results = b.run()

destinations = b.getDestinations()

out = open('times.csv', 'w')

# loop over the destinations and write out geoid and time to nearest high school
out.write('geoid,time\n')

for did in xrange(len(destinations)):
    # we reconstruct the GEOID10 as for some reason it isn't picked up in properties
    geoid = '%02d%03d%06d%04d' %\
            (destinations[did].properties['STATEFP10'], 
             destinations[did].properties['COUNTYFP10'],
             destinations[did].properties['TRACTCE10'],
             destinations[did].properties['BLOCKCE10'])
    
    # This is a very inefficient way to transpose a matrix, but we don't have numpy in jython
    time = min((r[did] for r in results))

    # write a row
    out.write('%s,%s\n' % (geoid, time / 60.0))
```