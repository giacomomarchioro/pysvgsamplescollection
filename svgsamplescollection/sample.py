from __future__ import print_function
from operator import itemgetter

class Sample:
    '''
    This class rappresnet a single sample. The first layer rappresent the
    sample itself. 
    '''
    def __init__(self,width,height,thickness='?',material='?',process='?',):
        self.width = width
        self.height = height
        self.elements = {}
        self.steps = {}
        self.current_step = 1
        self._layers_indexes = []
        self._treatments_indexes = []
        self._number_of_elements = 0
        self.add_layer(material,process,thickness,step=1)

    def add_layer(self,
                  material,
                  process,
                  thickness='?',
                  width_percent = 1,
                  height_percent = 1,
                  step=None,
                  xi = 0,
                  yi = 0,
                  xf = None,
                  yf = None,):
        
        if step is None: 
            step = self.current_step

        if xf == None:
                xf = self.width*width_percent

        if yf == None:
                yf = self.height*height_percent

        if xi >= xf or yi >= yf:
            raise ValueError("Intial coordinate exceed final!")

        if xf > self.width or yf > self.height:
            raise ValueError("Layer exceeds the sample dimension")

        info = {
         'id':self._number_of_elements, # consecutive ID
         'kind':'layer',
         'info':{
         'material':material,
         'process':process,
         'thickness_microns':thickness,
         'status':'?',
         'step':step, # linked step
         'applied_date':'?',
         'removed_date':'?'},
         'xi':xi,
         'yi':yi,
         'xf':xf,
         'yf':yf,
            }

        self.elements[self._number_of_elements] = info
        self._layers_indexes.append(self._number_of_elements)
        self._number_of_elements += 1


    def add_treatment(self,
                  process,
                  parameters,
                  layer=None,
                  width_percent = 1,
                  height_percent = 1,
                  step = None,
                  xi = 0,
                  yi = 0,
                  xf = None,
                  yf = None,):

        if step is None: 
            step = self.current_step

        if xf == None:
                xf = self.width*width_percent

        if yf == None:
                yf = self.height*height_percent

        if xi >= xf or yi >= yf:
            raise ValueError("Intial coordinate exceed final!")

        if xf > self.width or yf > self.height:
            raise ValueError("Layer exeed the sample dimension")

        if (layer is not None) and (layer not in self._layers_indexes):
            raise ValueError("Treatment applied to a layer that does not exists")


        info = {
         'id':self._number_of_elements, # consecutive ID
         'kind':'treatment',
         'info':{
         'process':process,
         'parameters':parameters,
         'status':'?',
         'applied_date':'?',
         'layer':layer,
         'step':step},
         'xi':xi,
         'yi':yi,
         'xf':xf,
         'yf':yf,
            }
        
        self.elements[self._number_of_elements] = info
        self._treatments_indexes.append(self._number_of_elements)
        self._number_of_elements += 1

    def get_layers(self):
        return itemgetter(*self._layers_indexes)(self.elements)
    
    def get_treatments(self):
        return itemgetter(*self._treatments_indexes)(self.elements)

if __name__ == "__main__":
    s = Sample(10,20,5,'metal','cast')
    print(s._number_of_elements)
    s.add_layer('laquer','brsh',width_percent=0.5)
    print(s._number_of_elements)
    s.add_treatment('clenaing','60W')
    print(s._number_of_elements)
    s.add_layer('coating','depostion',width_percent = 0.5)
    print(s._number_of_elements)

