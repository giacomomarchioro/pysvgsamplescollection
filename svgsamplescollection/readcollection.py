
from __future__ import print_function
import xml.etree.ElementTree as ET

name = "Test samples collection.svg"
tree = ET.parse(name)
root = tree.getroot()
records = {}
for child in root:
    records[child.attrib['id']] = child




#def get_samples_position():

def get_borders_positions(ids=[]):
    
    if type(ids) is int:
        ids = [ids]
        
    samples_positions = []
    for sample in records['samples_position']:
        if sample.tag == '{http://www.w3.org/2000/svg}rect':
            idi = int(sample.get('id'))
            if idi in ids or ids ==  []:
                xi = int(sample.get('x'))
                yi = int(sample.get('y'))
                xf = xi + int(sample.get('width'))
                yf = yi + int(sample.get('height'))
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