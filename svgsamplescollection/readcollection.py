from __future__ import print_function
import xml.etree.ElementTree as ET
import warnings


class ReadCollection():
    
    def __init__(self,path):
        self.path = path
        self.records = {}
        tree = ET.parse(self.path)
        self.root = tree.getroot()
        for child in self.root:
            self.records[child.attrib['id']] = child
        self.last_selection = None

    def _get_xiyixfyf(self,rectobj):
        '''
        Return initial x and y and final x and y coordinates from a rect xml
        object.
        '''
        xi = float(rectobj.get('x'))
        yi = float(rectobj.get('y'))
        xf = xi + float(rectobj.get('width'))
        yf = yi + float(rectobj.get('height'))
        return xi,yi,xf,yf
        

    def get_standard_position(self,idx=0):
        standard = self.records['standards'][idx]
        xi,yi,xf,yf = self._get_xiyixfyf(standard)
        return (xi,yi,xf,yf,'Standard')
    
    def get_collection_border(self,):
        border = self.records['collection_border']
        xi,yi,xf,yf = self._get_xiyixfyf(border)
        return (xi,yi,xf,yf,'Collection')
    
    
    def get_samples_position(self,ids=[]):
        
        if type(ids) is int:
            ids = [ids]
            
        samples_positions = []
        for sample in self.records['samples_position']:
            if sample.tag == '{http://www.w3.org/2000/svg}rect':
                idi = int(sample.get('id'))
                if idi in ids or ids ==  []:
                    xi,yi,xf,yf = self._get_xiyixfyf(sample)
                    samples_positions.append((xi,yi,xf,yf,idi))
                    
        if len(samples_positions) < len(ids):
            raise ValueError("Could not find some IDs you required!")
        return samples_positions
    
    
    def _get_positions_by_stroke(self,stroke,ids=[],WITH = '',WITHOUT=''):
        if type(ids) is int:
            ids = [ids]
        if type(WITH) is str: 
            WITH = [WITH]
        if type(WITHOUT) is str: 
            WITHOUT = [WITHOUT]
            
        samples_positions = []
        for sample in self.records["samples"]:
            if sample.tag == "{http://www.w3.org/2000/svg}rect":
                if sample.get("stroke") == stroke:
                    idi = int(sample.get('id'))
                    if idi in ids or ids ==  []:
                        t = sample[0].text # text with description
                        if WITH == [''] and WITHOUT == ['']:
                            xi,yi,xf,yf = self._get_xiyixfyf(sample)
                            samples_positions.append((xi,yi,xf,yf,idi))
                        
                        elif any(i in t for i in WITH):
                            if WITHOUT != [''] and any(i not in t for i in WITHOUT):
                                xi,yi,xf,yf = self._get_xiyixfyf(sample)
                                samples_positions.append((xi,yi,xf,yf,idi))
                            else:
                                xi,yi,xf,yf = self._get_xiyixfyf(sample)
                                samples_positions.append((xi,yi,xf,yf,idi))
        return samples_positions
        
    def get_layers_position(self,ids=[],WITH = '',WITHOUT=''):
    
            
        samples_positions = self._get_positions_by_stroke(stroke='yellow',
                                                     ids=ids,
                                                     WITH = WITH,
                                                     WITHOUT = WITHOUT,
                                                     )
                                              
        if len(samples_positions) < len(ids):
            warnings.warn("Could not find some layers with IDs you required!")
        self.last_selection = samples_positions
        return samples_positions
    
    def get_treatments_position(self,ids=[],WITH = '',WITHOUT=''):
        
        samples_positions = self._get_positions_by_stroke(stroke='magenta',
                                                     ids=ids,
                                                     WITH = WITH,
                                                     WITHOUT = WITHOUT,
                                                     )       
        if len(samples_positions) < len(ids):
            warnings.warn("Could not find some treatments with IDs you required!")
        self.last_selection = samples_positions
        return samples_positions    
        
    
    
    
    def get_polygons_where(self,ids = [],
                        treatment_with='',
                        layer_with='',
                        treatment_without='',
                        layer_without='',
                        show_results=False
                        ):
        if treatment_with != '' and layer_with != '':
            ly_w = self._unionbyID(self.get_layers_position(ids,WITH=layer_with))
            tr_w = self._unionbyID(self.get_treatments_position(ids,WITH=treatment_with))
            intrsc = {i:ly_w[i].intersection(tr_w[i]) for i in tr_w if i in ly_w}
        
        elif treatment_with !='' and layer_with == '':
            tr_w = self._unionbyID(self.get_treatments_position(ids,WITH=treatment_with))
            intrsc = {i:tr_w[i] for i in tr_w}
            
        elif treatment_with =='' and layer_with != '':
            ly_w = self._unionbyID(self.get_layers_position(ids,WITH=layer_with))
            intrsc = {i:ly_w[i] for i in ly_w}
            
        if layer_without != '':
            ly_wo = self._unionbyID(self.get_layers_position(ids,
                                                             WITH=layer_without))
            intrsc = self._diffbyID(intrsc,ly_wo)
        if treatment_without != '':
            tr_wo = self._unionbyID(self.get_treatments_position(ids,
                                                       WITH=treatment_without))
            intrsc = self._diffbyID(intrsc,tr_wo)
        
        if show_results:
            return self.show(intrsc)
        
        return intrsc
        
    def get_ROIs_position_where(self,ids = [],
                        treatment_with='',
                        layer_with='',
                        treatment_without='',
                        layer_without='',
                        show_results=False):
        '''
        Get the position of the ROIs as (xi,yi,xf,yf,ID) meeting the selection rules 
        calling the get_polygons_where function.
        '''
        intrsc = self.get_polygons_where(ids = ids,
                        treatment_with= treatment_with,
                        layer_with=layer_with,
                        treatment_without=treatment_without,
                        layer_without=layer_without)
        if show_results:
            return self.show(intrsc)
        
        coords = []
        for idx in intrsc: 
            x,y = intrsc[idx].exterior.coords.xy
            xi,xf = min(x),max(x)
            yi,yf = min(y),max(y)
            coords.append((xi,yi,xf,yf,idx))
        self.last_selection = coords
        return coords
    # Samples
        
    def _create_shapely_polygon(self,coords):
        from shapely.geometry import Polygon
        xi,yi,xf,yf,idx = coords
        p = Polygon([(xi,yi),
                 (xf,yi),
                 (xf,yf),
                 (xi,yf)])
        return p
    
    def _create_shapely_multipol(self,p):
        from shapely.geometry import MultiPolygon
        poligs = [ self._create_shapely_polygon(i) for i in p ]
        return MultiPolygon(poligs)
    
    def _unionbyID(self,listofcoord):
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
            p0 = self._create_shapely_polygon(d[i][0])
            for j in d[i][1:]:
                p0 = p0.union(self._create_shapely_polygon(j))
            res[i] = p0
        return res
    
    def _diffbyID(self,a,b):
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
    
    def show(self,dictobj):
        from shapely.geometry import MultiPolygon
        from shapely.affinity import scale
        poligs = [ self._create_shapely_polygon(i) for i in self.get_samples_position()]
        poligintr = [i for i in dictobj.values()]
        als = poligs + poligintr
        res = scale( MultiPolygon(als), yfact = -1, origin = (1, 0))
        #print(res)
        return res    

    def show_last_selction(self,):
       if self.last_selection is not None:           
           from shapely.geometry import MultiPolygon
           from shapely.affinity import scale
           poligs = [ self._create_shapely_polygon(i) for i in self.get_samples_position()]
           poligintr = [self._create_shapely_polygon(i) for i in self.last_selection]
           als = poligs + poligintr
           res = scale( MultiPolygon(als), yfact = -1, origin = (1, 0))
           #print(res)
           return res    
       else: 
           print('No selection in memory!')
