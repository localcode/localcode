sites = {
'proposed_sites':{ 'name': 'proposed_sites', 'cols':['ogc_fid', 'fid_1', 'fid_1_1', 'objectid', 'assrdata_m', 'perimeter', 'ain', 'phase', 'lot', 'unit', 'moved', 'tra', 'pcltype', 'subdtype', 'tract', 'usecode', 'block', 'udate', 'editorname', 'parcel_typ', 'unit_no', 'pm_ref', 'tot_units', 'shape_area', 'shape_len', 'has_bb', 'count_', 'sum_oid_', 'sum_latitu', 'sum_longit', 'sum_buff_d', 'count_1']},
}

micro = {
'parcel':{ 'name': 'parcel', 'cols':['ogc_fid', 'objectid', 'assrdata_m', 'perimeter', 'ain', 'phase', 'lot', 'unit', 'moved', 'tra', 'pcltype', 'subdtype', 'tract', 'usecode', 'block', 'udate', 'editorname', 'parcel_typ', 'unit_no', 'pm_ref', 'tot_units', 'shape_area', 'shape_len', 'has_bb']},
'streetlights':{ 'name': 'streetlights', 'cols':['ogc_fid', 'objectid', 'angle', 'icon_txt', 'icon_id', 'ls', 'pole_type', 'lum_abbr', 'lumen', 'watts', 'lgt_type', 'sup_dist', 'petition', 'project', 'clmd', 'cc_no', 'l_no', 'pm', 'tract', 'uud', 'dateenr', 'sce_dist', 'sce_acct', 'sce_pol_i', 'shielded', 'city', 'comments', 'efftransd']},
'tin_pts':{ 'name': 'tin_pts', 'cols':['ogc_fid', 'elevation', 'node_index']},
'censusblocks':{ 'name': 'censusblocks', 'cols':['ogc_fid', 'id', 'fipsstco', 'tract2000', 'block2000', 'stfid']},
        }

publictransportation = {
'localcentralbus':{ 'name': 'localcentralbus', 'cols':['ogc_fid', 'var_route', 'var_ident', 'var_direc', 'var_descr']},
'expressbuslines':{ 'name': 'expressbuslines', 'cols':['ogc_fid', 'var_route', 'var_ident', 'var_direc', 'var_descr']},
'rapidbuslines':{ 'name': 'rapidbuslines', 'cols':['ogc_fid', 'var_route', 'var_ident', 'var_direc', 'var_descr']},
'raillines':{ 'name': 'raillines', 'cols':['ogc_fid', 'path_id', 'miles', 'line', 'name']},
'metrobusstops':{ 'name': 'metrobusstops', 'cols':['ogc_fid', 'stopnum', 'along', 'at', 'long', 'lat']},
'localnoncentralbus':{ 'name': 'localnoncentralbus', 'cols':['ogc_fid', 'var_route', 'var_ident', 'var_direc', 'var_descr']},
        }

sewers = {
'countysewers':{ 'name': 'countysewers', 'cols':['ogc_fid', 'pipe_locn', 'type', 'diameter', 'street', 'p_length', 'jur', 'pc', 'mms', 'matl', 'umh', 'dmh', 'shape_len']},
'notcountysewers':{ 'name': 'notcountysewers', 'cols':['ogc_fid', 'shape_len']},
'channelpolygons':{ 'name': 'channelpolygons', 'cols':['ogc_fid', 'objectid', 'shape_leng', 'shape_area']},
        }

neighborhoood = {
'communityshuttlelines':{ 'name': 'communityshuttlelines', 'cols':['ogc_fid', 'var_route', 'var_ident', 'var_direc', 'var_descr']},
'landtypes':{ 'name': 'landtypes', 'cols':['ogc_fid', 'id', 'name', 'cat1', 'cat2', 'cat3', 'addrln1', 'addrln2', 'city', 'state', 'zip', 'desc']},
'garbagedist':{ 'name': 'garbagedist', 'cols':['ogc_fid', 'area', 'perimeter', 'disposal_', 'disposal_i', 'poly_', 'subclass', 'subclass_', 'rings_ok', 'name']},
'countylibraries':{ 'name': 'countylibraries', 'cols':['ogc_fid', 'city', 'addr_', 'addr2', 'name', 'phone']},
'secondaryschools':{ 'name': 'secondaryschools', 'cols':['ogc_fid', 'id', 'county', 'secondary', 'name']},
'transitdistricts':{ 'name': 'transitdistricts', 'cols':['ogc_fid', 'area', 'perimeter', 'name', 'adopted', 'ordinance', 'full_name', 'line', 'area_1', 'len', 'shape_area', 'shape_len']},
'communityplanareas':{ 'name': 'communityplanareas', 'cols':['ogc_fid', 'objectid', 'fid_1', 'plan_', 'symbol', 'acres', 'plan_leg', 'type', 'adopted', 'comm_name', 'globalid', 'shape_leng', 'shape_area']},
'soils':{ 'name': 'soils', 'cols':['ogc_fid', 'area', 'perimeter', 'class', 'area_acres', 'oid_', 'class_no', 'class_1', 'name', 'original']},
'watershedmanagementareas':{ 'name': 'watershedmanagementareas', 'cols':['ogc_fid', 'subclass', 'subclass_', 'rings_ok', 'rings_nok', 'id_', 'name1_', 'name2_', 'parts_', 'points_', 'name', 'shape_area', 'shape_len']},
'flooddistboundary':{ 'name': 'flooddistboundary', 'cols':['ogc_fid', 'myard', 'syard', 'length', 'dpw_mpm_fl']},
'waterpurveyors':{ 'name': 'waterpurveyors', 'cols':['ogc_fid', 'area', 'perimeter', 'wtr_eoc_', 'wtr_eoc_id', 'num', 'name1', 'name2', 'addr1', 'addr2', 'phone', 'ph2', 'source', 'color', 'area_1', 'len', 'shape_area', 'shape_len']},
'elementaryschools':{ 'name': 'elementaryschools', 'cols':['ogc_fid', 'id', 'county', 'elementary', 'name']},
'countyparks':{ 'name': 'countyparks', 'cols':['ogc_fid', 'park', 'addr1', 'addr2']},
        }

stormdrains = {
'catchbasins':{ 'name': 'catchbasins', 'cols':['ogc_fid', 'objectid']},
'gravitymains':{ 'name': 'gravitymains', 'cols':['ogc_fid', 'objectid', 'shape_leng']},
'openchannels':{ 'name': 'openchannels', 'cols':['ogc_fid', 'objectid', 'shape_leng']},
'stormdrains':{ 'name': 'stormdrains', 'cols':['ogc_fid', 'objectid', 'fnode_', 'tnode_', 'lpoly_', 'rpoly_', 'length', 'entity', 'layer', 'color', 'drain_name', 'text', 'distance', 'symbol', 'shape_len']},
'lateraldrains':{ 'name': 'lateraldrains', 'cols':['ogc_fid', 'objectid', 'shape_leng']},
        }

basins = {
'hydropoints':{ 'name': 'hydropoints', 'cols':['ogc_fid', 'objectid', 'comid', 'permanent_', 'fdate', 'resolution', 'gnis_id', 'gnis_name', 'reachcode', 'ftype', 'fcode', 'descriptio', 'canalditch', 'constructi', 'hydrograph', 'inundation', 'operationa', 'pipelinety', 'positional', 'relationsh', 'reservoirt', 'stage', 'specialuse']},
'groundwaterbasins':{ 'name': 'groundwaterbasins', 'cols':['ogc_fid', 'area', 'basin', 'symbol', 'number']},
'mediumwaterbasin':{ 'name': 'mediumwaterbasin', 'cols':['ogc_fid', 'objectid', 'gaz_id', 'area_acres', 'area_sqkm', 'states', 'loaddate', 'huc_10', 'hu_10_name', 'hu_10_type', 'hu_10_mod', 'shape_leng', 'shape_area']},
'largewaterbasin':{ 'name': 'largewaterbasin', 'cols':['ogc_fid', 'objectid', 'gaz_id', 'area_acres', 'area_sqkm', 'states', 'loaddate', 'huc_8', 'hu_8_name', 'shape_leng', 'shape_area']},
'localwaterbasin':{ 'name': 'localwaterbasin', 'cols':['ogc_fid', 'objectid', 'gaz_id', 'area_acres', 'area_sqkm', 'states', 'loaddate', 'huc_12', 'hu_12_name', 'hu_12_type', 'hu_12_mod', 'ncontrb_ac', 'ncontrb_sq', 'shape_leng', 'shape_area']},
'rain_50yr_24hr':{ 'name': 'rain_50yr_24hr', 'cols':['ogc_fid', 'id', 'z0yr_24hr']},
        }

billboards = {
'foundbillboards':{ 'name': 'foundbillboards', 'cols':['ogc_fid', 'objectid']},
'geocodedbillboards':{ 'name': 'geocodedbillboards', 'cols':['ogc_fid', 'oid_', 'address', 'city', 'state', 'latitude', 'longitude']},
        }

hydro = {
'hydrography':{ 'name': 'hydrography', 'cols':['ogc_fid', 'tlid', 'fnode', 'tnode', 'length', 'fedirp', 'fename', 'fetype', 'fedirs', 'cfcc', 'fraddl', 'toaddl', 'fraddr', 'toaddr', 'zipl', 'zipr', 'census1', 'census2', 'cfcc1', 'cfcc2', 'source']},
'waterbodies':{ 'name': 'waterbodies', 'cols':['ogc_fid', 'objectid', 'comid', 'permanent_', 'fdate', 'resolution', 'gnis_id', 'gnis_name', 'areasqkm', 'elevation', 'reachcode', 'ftype', 'fcode', 'descriptio', 'canalditch', 'constructi', 'hydrograph', 'inundation', 'operationa', 'pipelinety', 'positional', 'relationsh', 'reservoirt', 'stage', 'specialuse']},
'waterways':{ 'name': 'waterways', 'cols':['ogc_fid', 'objectid', 'comid', 'permanent_', 'fdate', 'resolution', 'gnis_id', 'gnis_name', 'lengthkm', 'reachcode', 'flowdir', 'wbareacomi', 'wbarea_per', 'ftype', 'fcode', 'shape_leng', 'enabled', 'descriptio', 'canalditch', 'constructi', 'hydrograph', 'inundation', 'operationa', 'pipelinety', 'positional', 'relationsh', 'reservoirt', 'stage', 'specialuse']},
        }

roads = {
'drp_trails':{ 'name': 'drp_trails', 'cols':['ogc_fid', 'name', 'designatio', 'status', 'shape_len']},
'rails':{ 'name': 'rails', 'cols':['ogc_fid', 'tlid', 'fnode', 'tnode', 'length', 'fedirp', 'fename', 'fetype', 'fedirs', 'cfcc', 'fraddl', 'toaddl', 'fraddr', 'toaddr', 'zipl', 'zipr', 'census1', 'census2', 'cfcc1', 'cfcc2', 'source']},
'freeways':{ 'name': 'freeways', 'cols':['ogc_fid', 'rte1_alf', 'type_name', 'shape_len']},
'roads':{ 'name': 'roads', 'cols':['ogc_fid', 'tlid', 'fnode', 'tnode', 'length', 'fedirp', 'fename', 'fetype', 'fedirs', 'cfcc', 'fraddl', 'toaddl', 'fraddr', 'toaddr', 'zipl', 'zipr', 'census1', 'census2', 'cfcc1', 'cfcc2', 'source']},
'bikeways':{ 'name': 'bikeways', 'cols':['ogc_fid', 'namea_alf', 'bike', 'class', 'status']},
        }


