import System
import System.Collections.Generic as SCG
import Rhino
import scriptcontext

import rhinoscriptsyntax as rs
from Rhino.FileIO import FileWriteOptions, FileReadOptions

def addRhinoLayer(layerName, layerColor=System.Drawing.Color.Black):
    """Creates a Layer in Rhino using a name and optional color. Returns the
    index of the layer requested. If the layer
    already exists, the color is updated and no new layer is created."""
    docLyrs = scriptcontext.doc.Layers
    layerIndex = docLyrs.Find(layerName, True)
    if layerIndex == -1:
        layerIndex = docLyrs.Add(layerName,layerColor)
    else: # it exists
        layer = docLyrs[layerIndex] # so get it
        if layer.Color != layerColor: # if it has a different color
            layer.Color = layerColor # reset the color
    return layerIndex

def layerAttributes(layerName, layerColor=System.Drawing.Color.Black):
    """Returns a Rhino ObjectAttributes object for a rhino layer with an optional color."""
    att = Rhino.DocObjects.ObjectAttributes()
    att.LayerIndex = addRhinoLayer(layerName, layerColor)
    return att

def deleteLayer(layerName, quiet=True):
    """Deletes a layer by Name. returns nothing."""
    layer_index = scriptcontext.doc.Layers.Find(layerName, True)
    settings = Rhino.DocObjects.ObjectEnumeratorSettings()
    settings.LayerIndexFilter = layer_index
    objs = scriptcontext.doc.Objects.FindByFilter(settings)
    ids = [obj.Id for obj in objs]
    scriptcontext.doc.Objects.Delete(ids, quiet)
    scriptcontext.doc.Layers.Delete(layer_index, quiet)

def bakeMany(listOfThings, objectAttributes=None):
    if not objectAttributes:
        objectAttributes = Rhino.DocObjects.ObjectAttributes()
    for thing in listOfThings:
        # move from specific to broad
        if isinstance(thing, Rhino.Geometry.Point3d):
            scriptcontext.doc.Objects.AddPoint(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Point):
            scriptcontext.doc.Objects.AddPoint(thing.Location, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Curve):
            scriptcontext.doc.Objects.AddCurve(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Surface):
            scriptcontext.doc.Objects.AddSurface(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Brep):
            scriptcontext.doc.Objects.AddBrep(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Mesh):
            scriptcontext.doc.Objects.AddSurface(thing, objectAttributes)
        elif isinstance(thing, Rhino.Geometry.Hatch):
            scriptcontext.doc.Objects.AddHatch(thing, objectAttributes)
        elif isinstance(thing, Rhino.Display.Text3d):
            scriptcontext.doc.Objects.AddText(thing, objectAttributes)
        else:
            print '''Unrecognized object type: %s''' % type(thing)

def deleteAll():
    """Deletes everything in the current Rhino scriptcontext.doc. Returns nothing."""
    guidList = []
    objType = Rhino.DocObjects.ObjectType.AnyObject
    objTable = scriptcontext.doc.Objects
    objs = objTable.GetObjectList(objType)
    for obj in objs:
        guidList.append(obj.Id)
    for guid in guidList:
        objTable.Delete(guid, True)

def exportFile(filePath,
        version=4,
        geomOnly=False,
        selectedOnly=False,
        ):
    '''Export a file.'''
    opt = FileWriteOptions()
    opt.FileVersion = version
    opt.WriteGeometryOnly = geomOnly
    opt.WriteSelectedObjectsOnly = selectedOnly
    return scriptcontext.doc.WriteFile(filePath, opt)

def exportLayers(layerNames, filePath, version=4):
    '''Export only the items on designated layers to a file.'''
    # save selection
    oldSelection = rs.SelectedObjects()
    # clear selection
    rs.UnselectAllObjects()
    # add everything on the layers to selection
    for name in layerNames:
        objs = scriptcontext.doc.Objects.FindByLayer(name)
        guids = [obj.Id for obj in objs]
        scriptcontext.doc.Objects.Select.Overloads[SCG.IEnumerable[System.Guid]](guids)
    # export selected items
    exportFile(filePath, version, selectedOnly=True)
    #clear selection
    rs.UnselectAllObjects()
    # restore selection
    if oldSelection:
        scriptcontext.doc.Objects.Select.Overloads[SCG.IEnumerable[System.Guid]](oldSelection)
    print 'exported %s' % filePath

# main script

if FilePath and DoExport and GeometryTree and LayerNames:
    numBranches = GeometryTree.BranchCount
    if numBranches == len(LayerNames):
        for i in range(GeometryTree.BranchCount):
            layer = LayerNames[i]
            if LayerColors and i < len(LayerColors):
                color = LayerColors[i]
            else:
                color = System.Drawing.Color.Black
            att = layerAttributes(layer, color)
            branchData = GeometryTree.Branch(i)
            bakeMany( branchData, att )
        exportLayers( LayerNames, FilePath )
        for lay in LayerNames:
            deleteLayer(lay)
    else:
        print '''Please ensure that there is one data tree branch
per layer name.'''
else:
    if DoExport:
        print '''Something is missing. Please make sure you input
a valid file path, a data tree of geometry (one branch per
layer), a list of layer names (one per branch), and that
you have entered 'True' into the 'DoExport' input.'''

