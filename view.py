import Rhino
import scriptcontext

from rhinopythonscripts.ViewTools import *
from rhinopythonscripts.LayerTools import *
from rhinopythonscripts.FileTools import *
from rhinopythonscripts.GeomTools import *

viewVect = Rhino.Geometry.Vector3d(0.8681,0.106589,-0.48481)


def importOne(sid, filetypes):
    path_mask = 'C:\\amigos\\dump\\%s-%s.%s' #id, type, ext
    files = [path_mask % (sid, t, '3dm') for t in filetypes]
    return fileGeometryDict(files)

# Rhino.Display.RhinoView.CreateShadedPreviewImage( imagePath, size, cPlane, ghostShade )
if __name__=='__main__':
    layers = [
            'bigcontours',
            'parcel-projected',
            'Default',
            'groundsurface',
            'smallcontours',
            'lateraldrains-projected',
            'gravitymains-projected',
            'othersites-projected',
            'catchbasins-projected',
            'billboards',
            'site-projected',
            ]
    filetypes = [
            'terrain',
            'borders',
            'billboards',
            'drains'
            ]
    layerD = importOne(24, filetypes)
    for k in layerD:
        print k
