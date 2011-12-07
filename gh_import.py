import Rhino

# for accesssing GH classes
import clr
clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree

# read geometry out of 3dm files and filter by layernames
if DoImport and FilePaths and LayerNames:

    layerTree = DataTree[Rhino.Geometry.GeometryBase]() # make a DataTree

    for filepath in FilePaths:
        model = Rhino.FileIO.File3dm.Read(filepath)
        if not model: continue
        for i, layer in enumerate(LayerNames):
            path = GH_Path(i)
            geometry = []
            objs = model.Objects.FindByLayer(layer)
            for obj in objs:
                geom = obj.Geometry
                geom.EnsurePrivateCopy()
                geometry.append(geom)
            layerTree.AddRange(geometry, path)
        # models can take up a considerable amount of
        # memory that we don't need, so get rid of it
        # after copying the geometry we want out of it
        model.Dispose()
