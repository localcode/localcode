import math

from Rhino.Geometry import *
from scriptcontext import doc

from rhinopythonscripts import GeomTools

angles = [6, 3, 2]
planes = [Plane.WorldXY.Rotate(math.pi/ a) for a in angles]
hardPlane = planes[2]
wildPlane = planes[1]
greenPlane = planes[0]

#class Site(smartLayerDict):
    #def __init__(self, smartLayerDict):
        #self.polygon
        #self.hardGrid
        #self.wildGrid
        #self.greenGrid
        #self.surface
        #self.busStops
        #self.accessEdges
        #self.

class GridPoint(object):
    def __init__(self, SmartPoint):
        self.point
        self.neighbors
        self.radius
        self.height
        self.axis
        self.slope
        self.


class SiteGrid(object):
    def __init__(self, polygon, surface):
        self.boundingbox
        self.boundary
        self.plane
        self.points
        self.circles

def siteGrids(smartLayerDict):
    greenGrid = GeomTools
    # get the polygon
    # get a bounding box for the polygon
    # make a point grid for that polygon
    # make a circle for each point


