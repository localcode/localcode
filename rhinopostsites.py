# Standard library imports
import json

# home-baked imports
from rhinopythonscripts.GeoJson2Rhino import *

class RhinoFeature():
    def __init__(self, geometry, attributes):
        self.geom = geometry
        self.att = attributes

    def asTuple(self):
        return (self.geom, self.att)

class Layer(object):
    """Used to hold information about individual layers."""
    def __init__(self, name):
        self.name = name
        self.name_in_db = name
        self.cols = None
        self.features = []
        self.color = None
        self.zColumn = None
        self.geoJson = None

    def __unicode__(self):
        return 'Layer: %s' % self.name

    def __str__(self):
        return unicode(self).encode('utf-8')


class Site(object):
    """Used to hold information about individual sites."""
    def __init__(self, id):
        self.id = None
        self.layers = []
        self.siteLayer = None
        self.terrainLayer = None
        self.connection = None
        self.json = None

    def __unicode__(self):
        return 'Site: id=%s' % self.id

    def __str__(self):
        return unicode(self).encode('utf-8')

def buildSiteLayer(rawLayer):
    layer = Layer(rawLayer['name'])
    if 'color' in rawLayer: # get the color if it exists
        layer.color = rlayer['color']
    jsonFeatures = rawLayer['contents']['features']
    for jsonFeature in jsonFeatures:
        # jsonToRhinoCommon comes from
        # rhinopythonscripts.GeoJson2Rhino
        geom = jsonToRhinoCommon(jsonFeature)
        att = jsonFeature['properties']
        rhFeature = RhinoFeature(geom, att)
        layer.features.append(rhFeature)
    return layer

def buildSite(id, layerCollection):
    site = Site(id)
    for rLayer in layerCollection['layers']:
        if len(rLayer['contents']['features']):
            site.layers.append(buildSiteLayer(rLayer))
    return site

def jsonsToPostSites(jsonSiteDict):
    sites = []
    for idKey in jsonSiteDict:
        layerColl = json.loads(jsonSiteDict[idKey])
        site = buildSite(idKey, layerColl)
        sites.append(site)
    return sites


