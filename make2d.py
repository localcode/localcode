import os
import shelve
import Rhino
import cPickle as pickle
from rhinopythonscripts import LayerTools, FileTools
from rhinopythonscripts.GeomTools import bakeMany
import System
from scriptcontext import doc
from System.Drawing import Rectangle
import rhinoscriptsyntax as rs

def rcmd(commandstring, echo=True, mask=True):
    if mask:
        premask = '-_%s '
        try:
            cmd = premask % commandstring
        except:
            print commandstring, 'failed to mask'
    else:
        cmd = commandstring
    result = Rhino.RhinoApp.RunScript(cmd, echo)
    if not result:
        print 'The following command failed:'
        print '   ',cmd
    return result

def rcmds(commands, echo=True, mask=True):
    for cmd in commands:
        rcmd( cmd, echo, mask )

def formatCmd( tup ):
    if tup[1]:
        return tup[0] % tup[1]
    else:
        return tup[0]

def storeNearRect(filePath):
    near = list(doc.Views.ActiveView.ActiveViewport.GetNearRect())
    far = list(doc.Views.ActiveView.ActiveViewport.GetFarRect())
    print 'view stored in %s' % filePath
    f = open( filePath, 'wb' )
    near.extend(far)
    pickle.dump( near, f )
    f.close()

def storeViewPoints(sids):
    outMask = '/amigos/db/%sviewPoints'
    for sid in sids:
        setView( sid )
        fPath = outMask % sid
        storeNearRect( fPath )

def chopCurvesToFrustum(curves):
    view = doc.Views.ActiveView.ActiveViewport
    nearPts = view.GetNearRect()
    farPts = view.GetFarRect()
    near = view.GetFrustumNearPlane()
    far = view.GetFrustumFarPlane()
    left = view.GetFrustumLeftPlane()
    right = view.GetFrustumRightPlane()
    top = view.GetFrustumTopPlane()
    bottom = view.GetFrustumBottomPlane()
    frustPts = nearPts.extend(farPts)
    frustBox = Rhino.Geometry.BoundingBox( frustPts )
    frustum = Rhino.Geometry.Brep.CreatefromBox( frustBox )


def bakeRaw( data, attributes = None, transVect=None):
    if type(data) not in (list, tuple):
        data = [data]
    elif type(data[0]) in (list, tuple, List):
        data = data[0]
    if attributes:
        att = attributes
    else:
        att = Rhino.DocObjects.ObjectAttributes()
    for thing in data:
        bakeMany(thing, att, transVect)
    doc.Views.ActiveView.Redraw()

def setView( sid ):
    # still don't know how to set up the size of the viewport.
    # this needs to be done manually
    f = open('/amigos/db/%sview' % sid, 'rb')
    view = pickle.load(f)
    f.close()
    if len(view) == 3:
        geom = view[0]
        vect = Rhino.Geometry.Vector3d(view[1])
        targ = view[2]
    else:
        return 'bad view data'


    vp = doc.Views.ActiveView.ActiveViewport
    vp.SetCameraDirection( vect, True)
    vp.SetCameraTarget(targ, True)
    bb = geom.GetBoundingBox(True)
    vp.ZoomBoundingBox( bb)
    doc.Views.ActiveView.Redraw()
    return view

def bakePickle( path, layer=None, attributes=None, transVector=None):
    if os.path.exists(path):
        try:
            f = open( path, 'rb' )
            data = pickle.load(f)
            f.close()
            bakeRaw(data, attributes, transVector)
            print 'baked %s to layer "%s"' % (path, layer)
        except:
            print 'trouble unpickling', path
    else:
        print '%s does not exist' % path

def getModelLayers(filePath, layers ):
    data = {}
    print 'getting %s' % filePath
    model = Rhino.FileIO.File3dm.Read( filePath )
    for layer in layers:
        geoms = []
        objs = model.Objects.FindByLayer( layer )
        for obj in objs:
            geom = obj.Geometry
            geom.EnsurePrivateCopy()
            geoms.append(geom)
        data[layer] = geoms
    model.Dispose()
    return data

def crossMatch(iter1, iter2):
    pairs = []
    for n in iter1:
        for m in iter2:
            pair = (n, m)
            pairs.append(pair)
    return pairs


def frustumX():
    view = doc.Views.ActiveView.ActiveViewport
    near = view.GetNearRect()
    far = view.GetFarRect()
    pairs = crossMatch( near, far )
    crvs = []
    for pair in pairs:
        crvs.append(Rhino.Geometry.Curve.CreateControlPointCurve(pair, 1))
    return crvs

def make2D(sid):
    # create frustum X
    frustumLines = frustumX()
    att = LayerTools.layerAttributes("viewportFramework", System.Drawing.Color.Cyan )
    bakeMany( frustumLines, att)
    cmds = [
        'SelAll',
        'Make2D Enter',
        'Invert Delete SetView World Top',
        'SelNone',
        'SelLayer Make2D::visible::lines::viewportframework',
        'SelLayer Make2D::hidden::lines::viewportframework',
        'ZS',
        'Delete',
        ]
    rcmds( cmds )

def exportPerspective( path ):
    # export the current view as an illustrator file
    cmds = [
            'SellAll',
            'Export "%s"' % path,
            'Enter',
            ]
    rcmds( cmds )


if __name__=='__main__':
    '''This Make2D script needs to do the following things:
        export linework for the topolines
        export linework for the site outline
        export linework for the other parcels
        export linework of the nearby busstops (and create circles for them)
        export linework for the terrain analysis curves and the drain arrows.
    '''

    scenes = [
            ('topo',), # maybe
            ('site','siteoutline'), # no
            ('parcels',), # maybe
            ('busstops',), # no
            ('terraindrain','terrainmeshlines','drainarrows',), # maybe
            ('plantwindows',), # no
            ]

    from site_ids import ids

    aiMask = 'C:\\amigos\\make2ds\\%s-%s.ai'

    for sid in ids[:1]:
        rcmd('SetView World Perspective')
        # set view
        setView(sid)

        for scene in scenes[:1]:

            outPath = aiMask % ( sid, scene )

            # delete everything
            FileTools.deleteAll()

            # get data
            if scene[0] == 'topo':
                layers = [
                        'bigcontours',
                        'smallcontours',
                        ]
                importPath = '/amigos/dump/%s-terrain.3dm' % sid
                data = getModelLayers( importPath, layers )
                print ', '.join(['%s:%s' % (k, len(data[k])) for k in data])
            else:
                data = {}
                if len(scene) > 1:
                    layers = scene[1:]
                else:
                    layers = scene
                for layer in layers:
                    fmask = '/amigos/db/%s%s' % (sid, layer)
                    f = open(fmask, 'rb')
                    data[layer] = pickle.load(f)
                    f.close()
            # bake data
            for key in data:
                layerAtt = LayerTools.layerAttributes( key )
                bakeMany( data[key], layerAtt )
            # do make2d or export AI file of current view
            exportPerspective( outPath )

            #make2D(sid)
            #cmds = [
                    #'SelAll',
                    #'Export "%s" Enter' % outPath,
                    #]



