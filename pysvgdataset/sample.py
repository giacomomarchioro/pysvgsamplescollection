from __future__ import print_function
from circle_sector import draw_mtf_aligment
import math



class Sample:
    '''
    This class rappresnet a single samle. The first layer rappresent the
    sample itself. 
    '''
    def __init__(self,width,height,material,process='?',thickness='?'):
        self.width = width
        self.height = height
        self.layers = {}
        self.treatments = {}
        self.markers = {}
        self.other = {}

        self.add_layer(material,process,thickness)

    def retrieve_id(self):
        idx =  len(self.layers) + len(self.treatments) + len(self.markers)
        + len(self.other)
        return idx

    def add_layer(self,
                  material,
                  process,
                  thickness='?',
                  width_percent = 1,
                  height_percent = 1,
                  xi = 0,
                  yi = 0,
                  xf = None,
                  yf = None,):

        if xf == None:
                xf = self.width*width_percent

        if yf == None:
                yf = self.height*height_percent

        if xi >= xf or yi >= yf:
            raise ValueError("Intial coordinate exceed final!")

        if xf > self.width or yf > self.height:
            raise ValueError("Layer exceeds the sample dimension")

        idx = self.retrieve_id()
        info = {'material':material,
         'process':process,
         'thickness':thickness,
         'status':'?',
         'id':idx,
         'xi':xi,
         'yi':yi,
         'xf':xf,
         'yf':yf,
         'kind':'layer'
            }

        self.layers[idx] = info

    def add_treatment(self,
                  process,
                  parameters,
                  layer=None,
                  duration='?',
                  width_percent = 1,
                  height_percent = 1,
                  xi = 0,
                  yi = 0,
                  xf = None,
                  yf = None,):

        if xf == None:
                xf = self.width*width_percent

        if yf == None:
                yf = self.height*height_percent

        if layer == None:
            layer = len(self.layers)

        if xi >= xf or yi >= yf:
            raise ValueError("Intial coordinate exceed final!")

        if xf > self.width or yf > self.height:
            raise ValueError("Layer exeed the sample dimension")

        if layer > len(self.layers):
            raise ValueError("Treatment applied to a layer that does not exists")



        idx = self.retrieve_id()

        info = {'idx':idx,
         'process':process,
         'duration':duration,
         'parameters':parameters,
         'status':'?',
         'layer':layer,
         'xi':xi,
         'yi':yi,
         'xf':xf,
         'yf':yf,
         'kind':'treatment'
            }

        self.treatments[idx] = info
