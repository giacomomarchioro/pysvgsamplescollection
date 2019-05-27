from __future__ import print_function
import xml.etree.ElementTree as ET

name = "Test dataset.svg"
tree = ET.parse(name)
root = tree.getroot()
records = {}
for child in root:
    records[child.attrib['id']] = child
