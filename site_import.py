###### THIS IS AN IronPython SCRIPT ######

# Import Standard Library
import os
import sys
import random
import cPickle

# Import .NET Libraries
import System

# Import Rhino Libraries
import Rhino
#import rhinoscriptsyntax as rs
import Rhino.RhinoApp as app
from scriptcontext import doc

# Project Imports
if 'rhinopythonscripts' in sys.modules:
    del sys.modules['rhinopythonscripts']
    print 'rhinopythonscripts cleared'

if 'GeoJson2Rhino' in sys.modules:
    del sys.modules['GeoJson2Rhino']
    print 'GeoJson2Rhino cleared'


#### LOCAL CODE LIBRARIES ####
#from rhinopythonscripts import GeoJson2Rhino
from rhinopostsites import *
from rhinopythonscripts import GeoJson2Rhino
from rhinopythonscripts.RunCPythonScript import run
from rhinopythonscripts.FileTools import *

# data import
from site_ids import ids
from sample_sites import jsons

def storeSites():
    sites = []
    for id in ids:
        sitejson = jsons[id]
        root = os.path.abspath('C:\Users\demonchaux\Dropbox\Amigos De Los Rios\siteJSONS')
        fname = os.path.join(root, ('%s.json' % id))

        f = open(fname, 'w')
        f.write(sitejson)
        f.close()

def saveSites(idList):
    for id in idList:
        #site = jsons[id]
        root = os.path.abspath('C:\Users\demonchaux\Dropbox\Amigos De Los Rios')
        rhroot = os.path.join(root, 'site3dms')
        rhfname = os.path.join(rhroot, ('%s-site.3dm' % id))
        # get the json
        guids = GeoJson2Rhino.load(site)
        saveDoc(rhfname)
        deleteAll()

def buildSite(siteId):
    rhroot = os.path.abspath('C:\\amigos\\dump')
    rhfname = os.path.join(rhroot, ('%s-site.3dm' % siteId))
    # get the json
    siteData = getSite(siteId)
    deleteAll()
    GeoJson2Rhino.load(siteData)
    exportFile(rhfname)

def buildWatersheds(siteId):
    rhroot = os.path.abspath('C:\\amigos\\dump')
    rhfname = os.path.join(rhroot, ('%s-watersheds.3dm' % siteId))
    # get the json
    siteData = getSite(siteId)
    deleteAll()
    GeoJson2Rhino.load(siteData)
    exportFile(rhfname)


def getRandy():
    seq = range(766)
    random.shuffle(seq)
    p = 'ids = [\n'
    e = '\n]'
    ids = ',\n'.join([('%s' % s) for s in seq[:50]])
    f = open('site_ids.py', 'w')
    f.write(p+ids+e)
    f.close()
    return ids

def testenv():
    for m in sys.modules:
        print m

def getSite(siteId):
    cModulePath = os.path.abspath('C:/Users/demonchaux/Dropbox/localcode/loadAmigosData.py')
    args = [siteId]
    out, err, code = run(cModulePath, args)
    #print code
    if code == 1: # it choked on something
        print err
    elif code == 0: # there was some result
        #print out
        return out

def addSite(site):
    # with either a site object or json, makes a site.
    if type(site) == str:
        return GeoJson2Rhino.load(site)

if __name__=='__main__':
    from site_ids import ids
    idList = range(462,767)[50:]
    doc.UndoRecordingEnabled = False
    doc.Views.RedrawEnabled = False
    for site in ids:
        print 'Building Site %s' % site
        #buildSite(site)
        buildWatersheds(site)
    doc.Views.RedrawEnabled = True
    doc.UndoRecordingEnabled = True

