import sys
import os

import Rhino

pathbits = [
        'C:\\Program Files (x86)',
        'Python26',
        'Lib',
        'site-packages'
        ]

importPath = os.path.join(*pathbits)
sys.path.append( importPath )

import networkx

G = networkx.Graph()
G.add_nodes_from(range(mesh.Vertices.Count))

def weight_function(i, j):
    p1 = Rhino.Geometry.Point3d((mesh.TopologyVertices[i]))
    p2 = Rhino.Geometry.Point3d((mesh.TopologyVertices[j]))
    base_weight = p1.DistanceTo(p2)
    deltaZ = p2.Z - p1.Z
    if deltaZ < 0.0:
        deltaZ *= -1
    return base_weight * deltaZ

for i in range(mesh.TopologyEdges.Count):
    pair = mesh.TopologyEdges.GetTopologyVertices(i)
    G.add_edge(pair.I, pair.J)
    weight = weight_function( pair.I, pair.J )
    G[pair.I][pair.J]['weight'] = weight

from_v = mesh.TopologyVertices.TopologyVertexIndex(from_node)
to_v = mesh.TopologyVertices.TopologyVertexIndex(to_node)

topology_list = networkx.algorithms.shortest_paths.generic.shortest_path(G, from_v, to_v, True)

a = [Rhino.Geometry.Point3d(mesh.TopologyVertices[v]) for v in topology_list]
