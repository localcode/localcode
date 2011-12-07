import os
import shelve
import Rhino
import cPickle as pickle
from rhinopythonscripts import LayerTools, FileTools
from rhinopythonscripts.GeomTools import bakeMany
from System.Collections.Generic import List
from scriptcontext import doc
from System.Drawing import Rectangle
import rhinoscriptsyntax as rs

mxwl = 'Maxwell_'

def __getMaterial( name):
    index = doc.Materials.Find( name, True )
    return index

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

def rcmds(commands, echo=True):
    for cmd in commands:
        rcmd(cmd, echo)

def formatCmd( tup ):
    if tup[1]:
        return tup[0] % tup[1]
    else:
        return tup[0]


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

def materialConfig( layerName, materialName, uv=None, run=False):
    if not materialName:
        return ''
    else:
        cmds = [
                ('SelNone',None),
                ('%sSetCurrentMaterial "%s"',(mxwl, materialName)),
                ('SelLayer "%s"', layerName),
                ('%sApplyCurrentMaterialToSelectedObjects', mxwl),
                ]
        if uv:
            cmds.extend( setUV(layerName, uv) )
        if run:
            rcmds(cmds)
        else:
            return cmds

def setUV( layerName, uv, run=False):
    if type(uv) in (int, float):
        u, v, w = uv, uv, uv
    elif len(uv) == 2:
        u, v, w = uv[0], uv[1], uv[0]
    elif len(uv) == 3:
        u, v, w = uv[0], uv[1], uv[2]

    cmds = [
            #('SelNone',None),
            #('SelLayer "%s"', layerName),
            ('ApplyBoxMapping 1 Diagonal 0 %s,%s,%s Yes Single 1 1',(u, v, w)),
            ]
    return cmds

def exportMXS( fileName, sl=8, time=9999, run=False):
    folder = os.path.split(fileName)[0]
    fname, ext = os.path.splitext(fileName)
    mxsName = fname + '.mxs'
    cmds = [
            ('%sOutputSettings ImagePath "%s" ImageType=%s _Enter', (mxwl, fileName, ext)),
            ('%sOutputSettings ScenePath "%s" _Enter', (mxwl, mxsName)),
            ('%sCameraSettings R V _Enter', mxwl),
            ('%sRenderSettings WriteMXI=No SamplingLevel=%s Time=%s _Enter ', (mxwl, sl, time)),
            ('%sRenderChannels Alpha=Yes MaterialID=Yes _Enter', mxwl),
            ('%sOutputSettings RenderSilent=yes _Enter', mxwl),
            ('%sRenderToMXS RenderScene _Enter', mxwl)
            ]
    if run:
        rcmds(cmds)
    else:
        return cmds




if __name__=='__main__':
    """
    This script needs to loop through each site, and then render the
    appropriate layers in sequence.

    For each site, I need to render:
        0 canopy with billboard and benches
        1 hardscape
        2 plantscape
        3 terrainmesh
        then I need to do a make2d with:
            4 everything?!



    For each render, I need to turn layers on and off and produce the mxs file

    For each layer:
        I need to assign and configure materials.
        for each material:
            I need to set UV tiling size

    """
    rs.EnableRedraw(False)


    materials = {
            # name: size
            'benches': 9.0,
            'canopy': 1.0,
            'billboard': 1.0,
            'new fur': (1.0, 3.0, 1.0),
            'fur light': 1.0,
            'hardscape': 1.0,
            'grayterrain': 9.0,
            }

    scenes ={
            0: 'toppings',
            1: 'hardscape',
            2: 'plants',
            3: 'terrain',
            4: 'linework',
            5: 'shadows',
            }


    from site_ids import ids

    layers = {
            'benchmeshes': ((0, 4, 5), 'benches'),
            'canopybreps':( (0,4, 5), 'canopy'),
            'drainareamesh':( (2,5), 'fur light'),
            'fullterrainmesh':((3,5), 'grayterrain'),
            'activebusstops':((4, ),),
            'siteoutline':((4, ),),
            'drainarrows':((4, ),),
            'billboards':( (0, 4, 5), 'billboard'),
            'parcels':((4, ),),
            'hardscapemesh': (( 1,5), 'hardscape'),
            }


    #i = 25

    s = 5
    for sid in ids:

        setView(sid)
        # unhide all and delete all
        [ rs.LayerVisible( n, True ) for n in layers ]
        FileTools.deleteAll()
        # get all the geometry
        for layer in layers:
            # make the layer
            att = LayerTools.layerAttributes(layer)
            path = '/amigos/db/%s%s' % (sid, layer)
            # get the geometry
            bakePickle( path, layer, att )

            if not rs.IsLayerEmpty( layer ) and len(layers[layer]) > 1:
                # set the material
                material = None
                material = layers[layer][1]
                matindex = __getMaterial( material )
                uv = materials[material]
                cmds = materialConfig( layer, material, uv )
                cmds = [formatCmd(c) for c in cmds]
                rcmds(cmds, False)

        # run through render frames
        for frame in range(6):

            # get the name of the frame/scene
            scene = scenes[frame]

            imageName = '/amigos/renders/%s-%03d.TIF' % (scene, sid )

            for layer in layers:
                # check that the layer has stuff
                if not rs.IsLayerEmpty( layer ):
                    if frame in layers[layer][0]: # on for this frame
                        #turn on layer
                        rs.LayerVisible( layer, True)

                    else:
                        # turn the layer off
                        rs.LayerVisible(layer, False)

            # export the mxs file
            renderCmds = exportMXS( imageName )
            renderCmds = [formatCmd(c) for c in renderCmds]

            # RUN THE RENDER COMMANDS
            rcmds( renderCmds, False )

            #print '\n'.join(renderCmds)

            #doc.Views.ActiveView.Redraw()

    rs.EnableRedraw(True)

