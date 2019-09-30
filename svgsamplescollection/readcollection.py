
from __future__ import print_function
import xml.etree.ElementTree as ET

name = "Test samples collection.svg"
tree = ET.parse(name)
root = tree.getroot()
records = {}
for child in root:
    records[child.attrib['id']] = child




#def get_samples_position():

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
    
def get_layers_position(ids=[]):
    if type(ids) is int:
        ids = [ids]
        
    samples_positions = []
    for sample in records["samples"]:
        if sample.tag == "{http://www.w3.org/2000/svg}rect":
            if sample.get("stroke") == "yellow":
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
    
    
records['samples']
# Samples position    
root[2]

def get_treatments_position():
    pass

def get_layer_position():
    pass

def get_areas_where(treatment=[],layer=[]):
    pass

# Samples
root[3]