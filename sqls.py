'''Useful sql queries for local code'''

def getContainingPolygon(fid, layer, polygonlayer):
    return """SELECT
    %(polygonlayer)s.ogc_fid
FROM
    %(polygonlayer)s
WHERE
    ST_Intersects(%(polygonlayer)s.wkb_geometry,
    (SELECT
        %(layer)s.wkb_geometry
    FROM
        %(layer)s
    WHERE
        %(layer)s.ogc_fid = %(fid)s))
;""" % {'fid':fid, 'layer':layer, 'polygonlayer':polygonlayer}

def isWithinDistance(fid, layer1, layer2, distance):
    return """SELECT ST_Distance(
;""" % {'fid':fid,'layer1':layer1,'layer2':layer2,'distance':distance,}

