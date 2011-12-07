import Rhino

"""
has_thoroughfare
billboard_distances
busstop_distances
bikeway_distances
trails_distances
access_distances
access_edges
"""

#points # a list of the hardscape points
test_val = 30

nears, nearPoints = zip(*[(i, points[i]) for i in range(len(points)) if access_distances[i] < access_filter_distance])


gridcloud = Rhino.Geometry.PointCloud(nearPoints)

def compareCloud(i): # point cloudss match input list index!
    item = gridcloud[i]
    pt = Rhino.Geometry.Point3d(item.X, item.Y, item.Z)
    return pt.DistanceTo( nearPoints[i] )

def closestCurve(curves, point, limit=1000):
    closest_distance = limit
    closest_curve = None
    for i, curve in enumerate(curves):
        out = curve.ClosestPoint( point, limit )
        if len(out) > 1:
            if out[0]:
                t = out[1]
            else:
                t = None
        if t:
            pt = curve.PointAt(t)
            dist = pt.DistanceTo(point)
            if  dist < closest_distance:
                closest_distance = dist
                closest_curve = i
    if closest_curve != None:
        return closest_curve
    else:
        return -1

closests = [closestCurve(access_edges, p, access_filter_distance) for p in nearPoints]
a = closests

