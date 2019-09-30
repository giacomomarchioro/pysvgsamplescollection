
from __future__ import print_function
import xml.etree.ElementTree as ET

name = "Test samples collection.svg"
tree = ET.parse(name)
root = tree.getroot()
records = {}
for child in root:
    records[child.attrib['id']] = child




#def get_samples_position():
def get_collection_border():
    border = records['collection_border']
    xi = float(border.get('x'))
    yi = float(border.get('y'))
    xf = xi + float(border.get('width'))
    yf = yi + float(border.get('height'))
    return (xi,yi,xf,yf,None)


def get_samples_positions(ids=[]):
    
    if type(ids) is int:
        ids = [ids]
        
    samples_positions = []
    for sample in records['samples_position']:
        if sample.tag == '{http://www.w3.org/2000/svg}rect':
            idi = int(sample.get('id'))
            if idi in ids or ids ==  []:
                xi = float(sample.get('x'))
                yi = float(sample.get('y'))
                xf = xi + float(sample.get('width'))
                yf = yi + float(sample.get('height'))
                samples_positions.append((xi,yi,xf,yf,idi))
                
    if len(samples_positions) < len(ids):
        raise ValueError("Could not find some IDs you required!")
    return samples_positions
    
def get_layers_position(ids=[],WITH = '',WITHOUT=''):
    if type(ids) is int:
        ids = [ids]
        
    samples_positions = []
    for sample in records["samples"]:
        if sample.tag == "{http://www.w3.org/2000/svg}rect":
            if sample.get("stroke") == "yellow":
                idi = int(sample.get('id'))
                if idi in ids or ids ==  []:
                    if WITH == '' and WITHOUT == '':
                        xi = float(sample.get('x'))
                        yi = float(sample.get('y'))
                        xf = xi + float(sample.get('width'))
                        yf = yi + float(sample.get('height'))
                        samples_positions.append((xi,yi,xf,yf,idi))
                    elif WITH in sample[0].text:
                        if WITHOUT != '' and WITHOUT not in sample[0].text:
                            xi = float(sample.get('x'))
                            yi = float(sample.get('y'))
                            xf = xi + float(sample.get('width'))
                            yf = yi + float(sample.get('height'))
                            samples_positions.append((xi,yi,xf,yf,idi))
                        else:
                            xi = float(sample.get('x'))
                            yi = float(sample.get('y'))
                            xf = xi + float(sample.get('width'))
                            yf = yi + float(sample.get('height'))
                            samples_positions.append((xi,yi,xf,yf,idi))
                            
                
    if len(samples_positions) < len(ids):
        raise ValueError("Could not find some IDs you required!")
    return samples_positions

def get_treatments_position(ids=[],WITH = '',WITHOUT=''):
    if type(ids) is int:
        ids = [ids]
        
    samples_positions = []
    for sample in records["samples"]:
        if sample.tag == "{http://www.w3.org/2000/svg}rect":
            if sample.get("stroke") == "magenta":
                idi = int(sample.get('id'))
                if idi in ids or ids ==  []:
                    if WITH == '' and WITHOUT == '':
                        xi = float(sample.get('x'))
                        yi = float(sample.get('y'))
                        xf = xi + float(sample.get('width'))
                        yf = yi + float(sample.get('height'))
                        samples_positions.append((xi,yi,xf,yf,idi))
                    elif WITH in sample[0].text:
                        if WITHOUT != '' and WITHOUT not in sample[0].text:
                            xi = float(sample.get('x'))
                            yi = float(sample.get('y'))
                            xf = xi + float(sample.get('width'))
                            yf = yi + float(sample.get('height'))
                            samples_positions.append((xi,yi,xf,yf,idi))
                        else:
                            xi = float(sample.get('x'))
                            yi = float(sample.get('y'))
                            xf = xi + float(sample.get('width'))
                            yf = yi + float(sample.get('height'))
                            samples_positions.append((xi,yi,xf,yf,idi))
                
    if len(samples_positions) < len(ids):
        raise ValueError("Could not find some IDs you required!")
    return samples_positions    
    
records['samples']
# Samples position    
root[2]



def get_areas_where(treatment_with='',
                    layer_with='',
                    treatment_without='',
                    layer_without=''):

    ly_w = _unionbyID(get_layers_position(WITH=layer_with))
    tr_w = _unionbyID(get_treatments_position(WITH=treatment_with))
    intrsc = {i:ly_w[i].intersection(tr_w[i]) for i in tr_w if i in ly_w}
    if layer_without != '':
        ly_wo = _unionbyID(get_layers_position(WITH=layer_without))
        intrsc = _diffbyID(intrsc,ly_wo)
    if treatment_without != '':
        tr_wo = _unionbyID(get_treatments_position(WITH=treatment_without))
        intrsc = _diffbyID(intrsc,tr_wo)
    return intrsc
    

# Samples
    
def _create_shapely_polygon(coords):
    from shapely.geometry import Polygon
    xi,yi,xf,yf,idx = coords
    p = Polygon([(xi,yi),
             (xf,yi),
             (xf,yf),
             (xi,yf)])
    return p

def _create_shapely_multipol(p):
    from shapely.geometry import MultiPolygon
    poligs = [ _create_shapely_polygon(i) for i in p ]
    return MultiPolygon(poligs)

def _unionbyID(listofcoord):
    '''
    Union of the samples with the same ID. Return a dictionary with a polygon
    associated with every ID
    '''
    from collections import defaultdict
    d = defaultdict(list)
    res = dict()
    for i in listofcoord:
        d[i[-1]].append(i)
    for i in d.keys():
        p0 = _create_shapely_polygon(d[i][0])
        for j in d[i][1:]:
            p0 = p0.union(_create_shapely_polygon(j))
        res[i] = p0
    return res

def _diffbyID(a,b):
    '''
    Given two dictionarys it subtracts b to a. If a not in b i keeps be as it is.
    '''
    diff= {}
    for i in a: 
        if i in b:
            res = a[i] - b[i]
            if res.is_empty:
                pass
            else:
                diff[i] = res
        else:
            diff[i] = a[i]
    return diff

def show(dictobj):
    from shapely.geometry import MultiPolygon
    from shapely.affinity import scale
    poligs = [ _create_shapely_polygon(i) for i in get_samples_positions()]
    poligintr = [i for i in dictobj.values()]
    als = poligs + poligintr
    res = scale( MultiPolygon(als), yfact = -1, origin = (1, 0))
    #print(res)
    return res    
ly_w = _unionbyID(get_layers_position(WITH='vermilion'))
tr_w = _unionbyID(get_treatments_position(WITH='acetone'))
intrsc = {i:ly_w[i].intersection(tr_w[i]) for i in tr_w if i in ly_w}
ly_wo = _unionbyID(get_layers_position(WITH='varnish'))
diff_ly = _diffbyID(intrsc,ly_wo)
tr_wo = _unionbyID(get_treatments_position(WITH='uv curing'))
diff_tr = _diffbyID(diff_ly,tr_wo)
    
root[3]