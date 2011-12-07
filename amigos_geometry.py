import sys
import math

import System

import Rhino
from Rhino.Geometry import *
import scriptcontext
from scriptcontext import doc

from rhinopythonscripts import FileUtils, LayerUtils, IntersectionTools, Smart, GeomTools, RangeTools
from rhinopythonscripts import RunCPythonScript as cScript
sqlScript = 'C:\\Users\\demonchaux\\Dropbox\\localcode\\runsql.py'

from sqls import *

from site_ids import ids

road_layers = [
        'freeways',
        'roads',
        ]

border_layers = [
        'site',
        'othersites',
        'parcel',
        ]

transportation_layers = [
        'bikeways',
        'drp_trails',
        'rapidbuslines',
        'expressbuslines',
        'raillines',
        'expressbuslines',
        'localcentralbus',
        'metrobusstops',
        ]

billboard_layers = [
        'foundbillboards',
        'geocodedbillboards',
        ]

water_layers = [
        'hydrography',
        'waterways',
        'waterbodies',
]

def getSiteLayerDict(index, types, layers):
    id = ids[index]
    fmask = 'C:\\amigos\\dump\\%s-%s.3dm'
    fpaths = [(fmask % (id, t)) for t in types]
    return FileUtils.importLayerDict(fpaths, layers)

def functionByLayer(function, layer):
    objs = doc.Objects.FindByLayer(layer)
    outList = []
    for obj in objs:
        outList.append(function(obj))

def projectCurvesToBrep(curves, brep, vector=Vector3d(0.0,0.0,1.0)):
    projCurves = []
    for curve in curves:
        projCurves.extend(curve.ProjectToBrep(curve, brep, vector, 0.001))
    return projCurves

def projectPointsToBrep(points, brep, vector=Vector3d(0.0,0.0,1.0)):
    return Intersect.Intersection.ProjectPointsToBreps([brep], points, vector, 0.001)

def layerDict(index, types, layers):
    for layer in layers:
        objs.append(doc.Objects.FindByLayer(layer))
    return dict(zip(layers, objs))

def p(anything):
    print anything

def makeDrains():
    drainLayers = ['openchannels',
              'gravitymains',
              'lateraldrains',
              ]
    drainColors = [
            System.Drawing.Color.MidnightBlue,
            System.Drawing.Color.Blue,
            System.Drawing.Color.CornflowerBlue,
            System.Drawing.Color.SkyBlue,
            ]

    for i in range(len(drainLayers)):
        lyr = drainLayers[i]
        newName = lyr+'-projected'
        lyrAtt = LayerUtils.layerAttributes(newName, drainColors[i]) # make the layer
        # get results
        resultPairs = IntersectionTools.smartCurveLayerProject(lyr, 'groundsurface', lyrAtt)
        # bake results
        for pair in resultPairs:
            scriptcontext.doc.Objects.AddCurve(pair[0], pair[1])
    # get the catchbasins
    srf = doc.Objects.FindByLayer('groundsurface')[0].Geometry
    rawPts = Smart.RhinoObjectsToSmartFeatures(doc.Objects.FindByLayer('catchbasins'))
    pt3ds = [pt.geom.Location for pt in rawPts]
    lowPts = Smart.replaceGeometries(rawPts, pt3ds)
    smrtPts = IntersectionTools.smartPointProject(lowPts, srf)
    newPts = [pt.geom for pt in smrtPts]
    circles = GeomTools.pointsToCircles(newPts, 0.5)
    smrtCircles = Smart.replaceGeometries(smrtPts, circles)
    lyrAtt = LayerUtils.layerAttributes('catchbasins-projected', drainColors[3])
    for circle in smrtCircles:
        doc.Objects.AddCircle(circle.geom, circle.objAttributes(lyrAtt))

def makeTerrainSurfaces():
    ptGrid = GeomTools.pointGrid(76, 76, 8, 8)
    # get the mesh
    try:
        mesh = doc.Objects.FindByLayer('tin_pts')[0].Geometry
        # make the points
        interpPoints = IntersectionTools.interpolatePointsToTerrainMesh(ptGrid, mesh)
        # make the surface
        srf = Rhino.Geometry.NurbsSurface.CreateFromPoints(interpPoints, 76, 76, 3, 3)
    except:
        print 'No contents on "tin_pts" layer'
        print 'flat ground created'
        srf = Rhino.Geometry.NurbsSurface.CreateFromPoints(ptGrid, 76, 76, 3, 3)
    # put it on the layer
    srfAtt = LayerUtils.layerAttributes('groundsurface', System.Drawing.Color.LightGray)
    doc.Objects.AddSurface(srf, srfAtt)
    srfBrep = Brep.CreateFromSurface(srf)

    contours = IntersectionTools.contourBrepInZ(srfBrep, 0.5)

    bigAtt = LayerUtils.layerAttributes('bigcontours', System.Drawing.Color.Black)
    smallAtt = LayerUtils.layerAttributes('smallcontours', System.Drawing.Color.DimGray)
    for i in range(len(contours)):
        if i % 10 == 0:
            # make a big contour
            for crv in contours[i]:
                doc.Objects.AddCurve(crv, bigAtt)
        else:
            # make a small contour
            for crv in contours[i]:
                doc.Objects.AddCurve(crv, smallAtt)

def makeTerrainFile(site_id):
    filePath = 'C:\\amigos\\dump\\%s-terrain.3dm' % site_id
    outLayers = [
            'groundsurface',
            'bigcontours',
            'smallcontours',
            ]
    FileUtils.exportLayers(outLayers, filePath)

def makeTerrains(idList):
    fmask = 'C:\\amigos\\dump\\%s-site.3dm'
    for id in idList:
        FileUtils.deleteAll()
        fpaths = [fmask % id]
        FileUtils.importFiles(fpaths)
        makeTerrainSurfaces()
        makeTerrainFile(id)

def makeDrainFiles(idList):
    fmask = 'C:\\amigos\\dump\\%s-%s.3dm'
    outMask = 'C:\\amigos\\dump\\%s-drains.3dm'
    types = ['site', 'terrain']
    outLayers = ['openchannels-projected',
              'gravitymains-projected',
              'lateraldrains-projected',
              'catchbasins-projected',
              ]
    for id in idList:
        FileUtils.deleteAll()
        fpaths = [(fmask % (id, t)) for t in types]
        FileUtils.importFiles(fpaths)
        makeDrains()
        outPath = outMask % id
        FileUtils.exportLayers(outLayers, outPath)

def addBillboards():
    # must have projected things already
    FileUtils.importFile('C:\\amigos\\templates\\billboardangled.3dm')
    FileUtils.importFile('C:\\amigos\\templates\\billboardstraight.3dm')
    lyrAtt = LayerUtils.layerAttributes('billboards')
    bbs = LayerUtils.getLayerGeometry('geocodedbillboards-projected')
    bbs.extend( LayerUtils.getLayerGeometry('foundbillboards-projected') )
    bbpoints = [bb.Location for bb in bbs]
    frwys = LayerUtils.getLayerGeometry('freeways-projected')
    roads = LayerUtils.getLayerGeometry('roads-projected')
    for pt in bbpoints:
        vector = GeomTools.vectorToClosestCurve(pt, frwys, 100.0)
        if vector: # freeway within 100m
            bbModel = LayerUtils.getLayerGeometry('billboardangled')
        else: # no freeways within 100meters
            vector = GeomTools.vectorToClosestCurve(pt, roads)
            bbModel = LayerUtils.getLayerGeometry('billboardstraight')
        GeomTools.moveMany( bbModel, Vector3d(pt) )
        angle = vector.VectorAngle( Vector3d.XAxis, vector, Plane.WorldXY )
        GeomTools.rotateMany( bbModel, angle, Vector3d.ZAxis, pt )
        GeomTools.bakeMany( bbModel, lyrAtt )
    LayerUtils.deleteLayer('billboardstraight')
    LayerUtils.deleteLayer('billboardangled')

def makeBillboardFiles(idList):
    fmask = 'C:\\amigos\\dump\\%s-%s.3dm'
    outMask = 'C:\\amigos\\dump\\%s-billboards.3dm'
    types = ['billboardpoints',
            'terrain',
            'roads',
            ]
    outLayers = ['billboards']
    for siteId in idList:
        FileUtils.deleteAll()
        fpaths = [(fmask % (siteId, t)) for t in types]
        FileUtils.importFiles(fpaths)
        addBillboards()
        outPath = outMask % siteId
        FileUtils.exportLayers(outLayers, outPath)

def makeProjectedFiles(idList, layerList, fileSuffix):
    fmask = 'C:\\amigos\\dump\\%s-%s.3dm'
    outMask = 'C:\\amigos\\dump\\%s-'+fileSuffix+'.3dm'
    types = ['site', 'terrain']
    outLayers = [s+'-projected' for s in layerList]
    for siteId in idList:
        FileUtils.deleteAll()
        fpaths = [(fmask % (siteId, t)) for t in types]
        FileUtils.importFiles(fpaths)
        for i, layer in enumerate(layerList):
            lyrAtt = LayerUtils.layerAttributes(outLayers[i]) # make the layer
            # determine geometry type
            sampleGeom = LayerUtils.getLayerGeometry(layer)
            if len(sampleGeom) > 0:
                if type(sampleGeom[0]) == Point:
                    resultPairs = IntersectionTools.smartPointLayerProject(layer, 'groundsurface', lyrAtt)
                    # bake results
                    for pair in resultPairs:
                        scriptcontext.doc.Objects.AddPoint(pair[0], pair[1])
                else:
                    resultPairs = IntersectionTools.smartCurveLayerProject(layer, 'groundsurface', lyrAtt)
                    # bake results
                    for pair in resultPairs:
                        scriptcontext.doc.Objects.AddCurve(pair[0], pair[1])
        outPath = outMask % siteId
        FileUtils.exportLayers(outLayers, outPath)

def importSiteFiles(siteId, types):
    fmask = 'C:\\amigos\\dump\\%s-%s.3dm'
    fpaths = [(fmask % (siteId, t)) for t in types]
    FileUtils.deleteAll()
    FileUtils.importFiles(fpaths)



if __name__ == '__main__':
    doc.UndoRecordingEnabled = False
    doc.Views.RedrawEnabled = False
    ##makeTerrains(range(435,767))
    ##makeDrainFiles(range(501,767))
    #makeProjectedFiles(range(448, 767), road_layers, 'roads')
    #makeProjectedFiles(range(438,767), billboard_layers, 'billboardpoints')
    #makeProjectedFiles(range(494, 767), border_layers, 'borders')
    #makeProjectedFiles(range(574, 767), transportation_layers, 'transportation')
    #makeProjectedFiles(range(395, 767), water_layers, 'water')
    makeBillboardFiles(range(370, 767))
    doc.Views.RedrawEnabled = True
    doc.UndoRecordingEnabled = True
    #addBillboards()
    #import random
    ##siteId = random.choice(ids)
    #siteId = ids[20]
    #types = [
            ##'site',
            #'terrain',
            #'billboards',
            #'drains',
            #'roads',
            #'borders',
            #'transportation',
            #'water',
            #]

    #importSiteFiles(siteId, types)



