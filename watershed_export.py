import Rhino
from scriptcontext import doc
from rhinopythonscripts import FileTools, LayerTools, GeomTools
from site_ids import ids
import cPickle as pickle

mask = '/amigos/dump/%s-watersheds.3dm'

layers = [
            'site',
            'localwaterbasin',
            'mediumwaterbasin',
            'largewaterbasin',
            'groundwaterbasins',
            'rain_50yr_24hr',
]

goodData = {
        'z0yr_24hr':'average rainfall',
        'hu_12_name':'local watershed',
        'hu_10_name':'area watershed',
        'basin':'area drainage basin',
        }

def pickleData( filePath, data ):
    f = open(filePath, 'wb')
    pickle.dump( data, f )
    f.close()

def unpickleData( filePath ):
    f = open(filePath, 'rb')
    data = pickle.load( f)
    f.close()
    return data

def objUserStringDictionary(obj):
    nvCollection = obj.Attributes.GetUserStrings()
    keys = list(nvCollection.AllKeys)
    values = [nvCollection.Get(k) for k in keys]
    return dict(zip(keys, values))


if __name__=='__main__':

    dataMask = '/amigos/db/%swaterdata'
    aiMask = 'C:\\amigos\\make2ds\\%s-watersheds.ai'
    for sid in ids:
        pickleFile = dataMask % sid
        aiFile = aiMask % sid
        siteData = {}
        # delete everything
        FileTools.deleteAll()
        # open file,
        model = Rhino.FileIO.File3dm.Read( mask % sid )
        # get curves by layer, along with names
        for layer in layers:
            geoms = []
            objs = model.Objects.FindByLayer(layer)
            for obj in objs:
                data = objUserStringDictionary(obj)
                for k in data:
                    if k in goodData:
                        if goodData[k] not in siteData:
                            siteData[goodData[k]] = [data[k]]
                        else:
                            siteData[goodData[k]].append( data[k] )
                geom = obj.Geometry
                geom.EnsurePrivateCopy()
                geoms.append( geom )
            layerAtt = LayerTools.layerAttributes( layer )
            if layer != 'site':
                GeomTools.bakeMany( geoms, layerAtt )
            else:
                siteCrv = geoms[0]
                bbox = siteCrv.GetBoundingBox(False)
                minPt, maxPt = bbox.Min, bbox.Max
                xyPlane = Rhino.Geometry.Plane.WorldXY
                rect = Rhino.Geometry.Rectangle3d( xyPlane, minPt, maxPt )
                newCrv = rect.ToNurbsCurve()
                GeomTools.bakeMany( [newCrv], layerAtt )

        # save watershed info
        pickleData( pickleFile, siteData )
        #print unpickleData( pickleFile )
        # zoom to everything
        Rhino.RhinoApp.RunScript('-_ZE ', True)
        # export to illustrator
        Rhino.RhinoApp.RunScript('-_SelAll ', True)
        Rhino.RhinoApp.RunScript(('-_Export "%s" Enter ' % aiFile), True)

        # dispose model
        model.Dispose()

