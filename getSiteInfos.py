from site_ids import ids
from postsites.sqls import nearest, getInfo
from postsites.configure import dbinfo
from postsites import DataSource
from amigos_layers import sites, roads, basins
import xlwt


def get_datas(sids, siteCols, siteLayer, nearLayers):
    ds = DataSource(dbinfo)
    ds._connect()
    datas = {}
    for sid in sids:
        sitesql = getInfo(siteLayer, siteCols, sid)
        datas[sid] = {}
        datas[sid][siteLayer] = dict(zip(siteCols, *ds._run(sitesql)))
        for layer in nearLayers:
            cols = nearLayers[layer]['cols']
            sql = nearest( siteLayer, layer, 1000, sid, cols )
            data = ds._run(sql)
            if len(data) > 0:
                vals = data[0]
            else:
                vals = []
            datas[sid][layer] = dict(zip(cols, vals))
    ds._close()
    return datas

def datasToXLS(datas, filepath):
    wkbk = xlwt.Workbook()
    sht = wkbk.add_sheet('data')
    headers = []
    rows = []
    for sid in datas:
        rowDict = datas[sid]
        vals = [sid]
        for k in rowDict:
            for k2 in rowDict[k]:
                vals.append(rowDict[k][k2])
        rows.append(vals)


    firstRow = datas[rows[0][0]]
    for key in firstRow:
        for key2 in firstRow[key]:
            colname = '%s-%s' % (key, key2)
            headers.append(colname)
    for i, row in enumerate(rows):
        r = i + 1
        for j, val in enumerate(row):
            c = j
            sht.write(r, c, row[j])
    for i, col in enumerate(headers):
        r = 0
        c = i +1
        sht.write(r, c, col)
    wkbk.save(filepath)
    pass


if __name__=='__main__':
    xlsFile = 'amigos_site_data-1.xls'
    nearLayers = {
'soils':{ 'name': 'soils', 'cols':['class', 'name']},
'groundwaterbasins':{ 'name': 'groundwaterbasins', 'cols':['ogc_fid', 'basin' ]},
'mediumwaterbasin':{ 'name': 'mediumwaterbasin', 'cols':['ogc_fid', 'hu_10_name']},
'largewaterbasin':{ 'name': 'largewaterbasin', 'cols':['ogc_fid','hu_8_name']},
'localwaterbasin':{ 'name': 'localwaterbasin', 'cols':['ogc_fid', 'hu_12_name']},
            }
    layer = 'proposed_sites'
    site_cols = sites[layer]['cols']
    ids = range(45,48)
    data = get_datas(ids, site_cols, layer, nearLayers)
    #print data
    #datasToXLS( data, xlsFile )


