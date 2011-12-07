import sys

if 'rhinopythonscripts' in sys.modules:
    del sys.modules['rhinopythonscripts']

## this is an IronPython script
import Rhino
import scriptcontext


import rhinopythonscripts
from rhinopythonscripts.FileUtils import deleteAll, exportFile
from rhinopythonscripts.RunCPythonScript import run as runC
from rhinopythonscripts.GeoJson2Rhino import load as jsonLoad

cModule = 'C:\\Users\\demonchaux\\Dropbox\\localcode\\loadAmigosData.py'

def createJsonFiles(idList):
    froot = 'C:\\amigos\\dump\\%s-site.3dm'
    for id in idList:
        deleteAll()
        print "loading site %s" % id
        out, err, code = runC(cModule, [id])
        if code == 1: # there's an error
            print err
        else:
            print 'building geometry'
            guids = jsonLoad(out)

            fpath = froot % id
            exportFile(fpath)
            print "Successfully wrote %s" % fpath

    print 'done'

if __name__=='__main__':
    idList = range(767)
    createJsonFiles(idList)
