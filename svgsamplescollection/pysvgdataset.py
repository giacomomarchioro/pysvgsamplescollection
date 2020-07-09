'''
Py
'''
from __future__ import print_function
from .circle_sector import draw_mtf_aligment 

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
        self._alignment_MTF_standards = []
        self._samples_coordinates = []
        self._samples_ID = []
        
    def find_cols_rows(self):
        num_samples = self.number_of_samples
        hor_margin = self.margin_left_mm + self.margin_right_mm
        usable_w = self.data_set_dimension[0] - hor_margin
        ver_margin = self.margin_top_mm + self.margin_bottom_mm
        usable_h = self.data_set_dimension[1] - ver_margin
        space_required_for_sample = self.samples_dimensions[0]+self.minh_spacing_mm
        effective_space = usable_w+self.minh_spacing_mm
        print(effective_space)
        print(space_required_for_sample)
        samples_per_row = effective_space/space_required_for_sample
        print(samples_per_row)
        max_number_of_rows = (usable_h-self.minv_spacing_mm)%self.samples_dimensions[1]
        print(samples_per_row)
        if  samples_per_row*max_number_of_rows >= num_samples:
            self.rows = int(round(num_samples/float(samples_per_row)))
            self.cols = samples_per_row
        else:
            print("Max number of samples: %s" %(samples_per_row*max_number_of_rows))
            print("Too many samples! Try to decrease margins or spacing!")
    
    def findcord(self):
        xlen = self.samples_dimensions[0]+self.minh_spacing_mm
        xs = [self.margin_left_mm + xlen*i for i in range(self.cols) ]
        ylen = self.samples_dimensions[1]+self.minv_spacing_mm
        ys = [self.margin_top_mm + ylen*i for i in range(self.rows) ]
        counter = 0
        for y in ys:
            for x in xs:
                if counter < self.number_of_samples:
                    self._samples_coordinates.append([x,y])
                    counter +=1
                else:
                    continue
    def insert_alignment_MTF_standard(self):
        minsp = min([self.margin_top_mm,
             self.margin_bottom_mm,
             self.margin_left_mm, 
        self.margin_right_mm,])
        
        r = minsp*0.8
        spacing = minsp/2.
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
   xmlns="http://www.w3.org/2000/svg">""" %(x,y) +"\n")
            ytit = self.margin_top_mm/2
            xtit = self.margin_left_mm
            f.write( r"""<text 
   x="%smm"
   y="%smm"
   font-family="Verdana"
   font-size="20"
   fill="blue"> 
   DATASET: %s  </text>"""%(xtit,ytit,self.name)+"\n")
            if border_as_cutline:
                f.write( r"""<rect
   x="0mm"
   y="0mm"
   width="%smm"
   height="%smm"
   stroke="red"
   stroke-width="1"
   fill-opacity="0"  />""" %(x,y)+"\n" )
            f.write( r"""<g id="samples">"""+"\n" )
            for index, i in enumerate(self._samples_coordinates):
                ids = self._samples_ID[index]
                f.write( r"""   <rect
      x="%smm"
      y="%smm"
      id="%s"
      width="%smm"
      height="%smm"
      stroke="red" 
      stroke-width="1" 
      fill-opacity="0" /> """ %(i[0],i[1],ids,w,h)+"\n")
                ty = i[1] - self.text_y
                
                f.write( r"""   <text
      x="%smm" 
      y="%smm"
      font-family="Verdana"
      font-size="10"
      fill="blue" > 
      ID: %s  </text>""" %(i[0],ty,ids)+"\n")
            f.write( r"</g>"+"\n" )
            
        
            if self._alignment_MTF_standards != []:
                f.write(r"""<g stroke="none" fill="lime">"""+"\n")
                for i in self._alignment_MTF_standards:
                    f.write(i+"\n")
                f.write(r"</g>")
            
            #Close the file
            f.write(r"</svg>")
                

if __name__ == '__main__':
    h = Dataset()
    s = sizes()
    h.name = 'Test'    
    h.data_set_dimension = s.hA4
    h.samples_dimensions = s.hMicroscope_slide
    h.number_of_samples = 13
    h.find_cols_rows()
    #h.cols, h.rows = 1,1
    h.findcord()
    h.insert_alignment_MTF_standard()
    h.save_svg()
