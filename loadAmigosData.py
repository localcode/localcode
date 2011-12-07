import json
from amigos_layers import *
from postsites import loadFromXlsConfigurationFile, DataSource
from postsites import makeXlsConfigurationFile
from postsites.configure import dbinfo
from site_ids import ids

def readFolder():
    folder = 'C:\\Users\\demonchaux\\Dropbox\\Amigos De Los Rios\\Our Maps\\Parcel'
    #folder = "C:\\Users\\demonchaux\\Dropbox\\Amigos De Los Rios\\Data June 7th"
    #folder = "C:\\Users\\demonchaux\\Dropbox\\Amigos De Los Rios"
    config_file = makeXlsConfigurationFile(folder, 'parcels.xls')
    print config_file

def loadXls():
    # load everything in
    xlsFile = 'parcels.xls'
    ds, results = loadFromXlsConfigurationFile( xlsFile, dbinfo, verbose=True, skipfailures=True)
    print results
    #print '\n'.join(results)
    print '\n'.join([lay.name for lay in ds.config.layers])

def seeLayers():
    ds = DataSource( dbinfo )
    ds.viewLayers('layers.py')

def loadWithColumns(site_id):
    #sites.update(micro)
    #sites.update(stormdrains)
    #sites.update(sewers)
    #sites.update(publictransportation)
    sites.update(basins)
    #sites.update(billboards)
    sites.update(hydro)
    #sites.update(roads)
    ds = DataSource(dbinfo)
    ds.loadLayerDict(sites)
    ds.config.setSiteLayer('proposed_sites')
    #ds.config.setTerrainLayer('tin_pts')
    #ds.config.terrainLayer.zColumn = 'elevation'
    ds.config.siteRadius = 1000
    return ds.getSiteJson( site_id )

def createJsonFiles(idList):
    froot = 'C:\\amigos\\dump\\%s-site.json'
    for id in idList:
        print "loading site %s" % id
        try:
            json = ds.loadWithColumns
        except:
            print "error loading %s" % id
        fpath = froot % id
        f = open(fpath, 'w')
        f.write(json)
        f.close()
        print "Successfully wrote %s" % fpath
    print done


if __name__=='__main__':

    import sys
    siteId = sys.argv[1]
    siteJson = loadWithColumns(siteId)
    print siteJson
    #idList = range(20)
    #createJsonFiles(idList)

    #seeLayers()



