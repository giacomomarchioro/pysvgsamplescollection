'''
Py
'''
from __future__ import print_function
from circle_sector import draw_mtf_aligment
import math 

class sizes:
    def __init__(self):
        self.vMicroscope_slide = [ 25, 70, 1]
        self.vMicroscope_slide_geo = [50, 75, 1]
        self.vMicroscope_slide_petro = [27, 46, 1]
        self.vA7 = [ 81, 114, 0] 
        self.vA4 = [210, 297, 0]
        self.hMicroscope_slide = [ 70, 25, 1]
        self.hMicroscope_slide_geo = [75, 50, 1]
        self.hMicroscope_slide_petro = [46, 27, 1]
        self.hA7 = [ 114, 81, 0] 
        self.hA4 = [297,210, 0]


class Sample:
    def __init__(self):
        self.width = 0
        self.height = 0 
        self.layers = []
        self.treatments = []
        self.markers = []

class Dataset:
    def __init__(self,name = 'Dataset'):
        self.name = name
        self.data_set_dimension = ['x','y']
        self.number_of_samples = None 
        self.samples_dimensions = ['x','y']
        self.margin_top_mm = 20 
        self.margin_bottom_mm = 20 
        self.margin_left_mm = 20 
        self.margin_right_mm = 20
        self.text_y = 2
        self.rows = None
        self.cols = None
        self.minh_spacing_mm = 10
        self.minv_spacing_mm = 10
        self.title_font_size = 10
        self.label_font_size = 10
        self._alignment_MTF_standards = []
        self._samples_coordinates = []
        self._samples_ID = []
        
    def find_cols_rows(self):
        '''
        This method find the max number of samples that can be fit in the
        dataset. 
        '''
        num_samples = self.number_of_samples
        hor_margin = self.margin_left_mm + self.margin_right_mm
        usable_w = self.data_set_dimension[0] - hor_margin
        ver_margin = self.margin_top_mm + self.margin_bottom_mm
        usable_h = self.data_set_dimension[1] - ver_margin
        hspace_smpl_require = self.samples_dimensions[0]+self.minh_spacing_mm
        vspace_smpl_require = self.samples_dimensions[1]+self.minh_spacing_mm
        #Actually we have to consider that the last sample can be place next to
        # the margin, so we add the spacing to the effective space
        effective_space = usable_w+self.minh_spacing_mm
        print(effective_space)
        print(hspace_smpl_require)
        samples_per_row = effective_space/hspace_smpl_require
        print(samples_per_row)
        
        max_number_of_rows = (usable_h+self.minv_spacing_mm)/vspace_smpl_require
        print('maxnumber',max_number_of_rows)
        if  samples_per_row*max_number_of_rows >= num_samples:
            self.rows = int(math.ceil(num_samples/float(samples_per_row)))
            self.cols = samples_per_row
        else:
            print("Max number of samples: %s" %(samples_per_row*max_number_of_rows))
            print("Too many samples! Try to decrese margins or spacing!")
    
    def findcord(self):
        xlen = self.samples_dimensions[0]+self.minh_spacing_mm
        xs = [self.margin_left_mm + xlen*i for i in range(self.cols) ]
        ylen = self.samples_dimensions[1]+self.minv_spacing_mm
        ys = [self.margin_top_mm + ylen*i for i in range(self.rows) ]
        counter = 0
        
        for y in ys:
            for x in xs:
                print(x,'  ',y)
                if counter < self.number_of_samples:
                    self._samples_coordinates.append([x,y])
                    counter +=1
                else:
                    print(counter)
                    continue
                
    def insert_alignment_MTF_standard(self):
        minsp = min([self.margin_top_mm,
             self.margin_bottom_mm,
             self.margin_left_mm, 
        self.margin_right_mm,])
        
        r = minsp*0.9
        spacing = minsp/2.
        r = spacing/2
        x,y,_ = self.data_set_dimension
        #Top left
        utl = draw_mtf_aligment(xcenter=spacing, ycenter=spacing,r=r)
        #Top right
        utr = draw_mtf_aligment(xcenter= x - spacing, ycenter=spacing,r=r) 
        #Bottom left
        btl = draw_mtf_aligment(xcenter=spacing, ycenter= y - spacing,r=r)
        #Bottom right
        btr = draw_mtf_aligment(xcenter= x - spacing, ycenter= y - spacing,r=r)
        self._alignment_MTF_standards = utl + utr + btl + btr
    
    
    def save_svg(self,border_as_cutline = True): 
        if self._samples_ID == []:
            self._samples_ID = range(self.number_of_samples)
        with open('%s.svg' %self.name,'w') as f:
            x,y = self.data_set_dimension[0],self.data_set_dimension[1]
            w,h = self.samples_dimensions[0],self.samples_dimensions[1]
            f.write(r"""<svg version="1.1"  
   baseProfile="full" width="%smm" 
   height="%smm"
   viewBox="0 0 %s %s"
   xmlns="http://www.w3.org/2000/svg">""" %(x,y,x,y) +"\n")
            ytit = self.margin_top_mm/2
            xtit = self.margin_left_mm
            f.write( r"""<text 
   x="%s"
   y="%s"
   font-family="Verdana"
   font-size="10"
   fill="blue"> 
   DATASET: %s  </text>"""%(xtit,ytit,self.name)+"\n")
            if border_as_cutline:
                f.write( r"""<rect
   x="0"
   y="0"
   width="%s"
   height="%s"
   stroke="red"
   stroke-width="1"
   fill-opacity="0"  />""" %(x,y)+"\n" )
            f.write( r"""<g id="samples">"""+"\n" )
            for index, i in enumerate(self._samples_coordinates):
                ids = self._samples_ID[index]
                f.write( r"""   <rect
      x="%s"
      y="%s"
      id="%s"
      width="%s"
      height="%s"
      stroke="red" 
      stroke-width="0.5" 
      fill-opacity="0" /> """ %(i[0],i[1],ids,w,h)+"\n")
                ty = i[1] - self.text_y
                
                f.write( r"""   <text
      x="%s" 
      y="%s"
      font-family="Verdana"
      font-size="5"
      fill="blue" > 
      ID: %s  </text>""" %(i[0],ty,ids)+"\n")
            f.write( r"</g>"+"\n" )
            
        
            if self._alignment_MTF_standards != []:
                f.write(r"""<g stroke="none" fill="blue">"""+"\n")
                for i in self._alignment_MTF_standards:
                    f.write(i+"\n")
                f.write(r"</g>")
            
            #Close the file
            f.write(r"</svg>")
                

if __name__ == '__main__':
    h = Dataset()
    s = sizes()
    h.name = 'Test2'    
    #h.data_set_dimension = s.hMicroscope_slide_petro
    h.data_set_dimension = s.hA4
    h.samples_dimensions = s.hMicroscope_slide
#    h.margin_top_mm = 2 
#    h.margin_bottom_mm = 2 
#    h.margin_left_mm = 2 
#    h.margin_right_mm = 2
#    h.samples_dimensions = [5,5,0]
    h.number_of_samples = 12 
    h.find_cols_rows()
    #h.cols, h.rows = 1,1
    h.findcord()
    h.insert_alignment_MTF_standard()
    h.save_svg()


## for sample in dataset.samples[0:5]:
#       sample.add_layer(description = "varnish", ends = (half,half))
#       sample.add_treatment(description = "laser cleaning", params = {"watt":100, "time (sec): 3}, xyorigin = (10,10) xyend = (50,50))
    
    # Prit masks 