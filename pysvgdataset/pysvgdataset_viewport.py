'''
Py
'''
from __future__ import print_function
from circle_sector import draw_mtf_aligment
from sample import Sample
import math


    
  


class Dataset:
    
    class sizes:
        def __init__(self,d,kind):
            self._d = d
            self._kind = kind
        
        def _assign(self, dim, kind):
            if kind == 'dataset':
                self._d.dataset_dimension = dim
            if kind == 'sample':
                self._d.sample_dimension = dim
            
        def vMicroscope_slide(self):
           self._assign([ 25, 70, 1],self._kind)
            
        def vMicroscope_slide_geo(self): 
           self._assign([50, 75, 1],self._kind)
            
        def vMicroscope_slide_petro(self): 
           self._assign([27, 46, 1],self._kind)
            
        def vA7(self):
           self._assign([81, 114, 0],self._kind)
            
        def vA4(self): 
           self._assign([210, 297, 0],self._kind)
            
        def Microscope_slide(self):
           self._assign([ 70, 25, 1],self._kind)
            
        def Microscope_slide_geo(self):
           self._assign([75, 50, 1],self._kind)
            
        def Microscope_slide_petro(self): 
           self._assign([46, 27, 1],self._kind)
            
        def A7(self):
           self._assign([ 114, 81, 0],self._kind)
            
        def A4(self):
           self._assign([297,210, 0],self._kind)
        
        def custom(self,w,h,d):
           self._assign( [w,h,d],self._kind)
            
    def __init__(self,name = 'Dataset'):
        self.name = name
        self.dataset_dimension = ['x','y']
        self.samples = []
        self.number_of_samples = None
        self.samples_dimension = ['x','y']
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
        self.set_dataset_dimension = self.sizes(self,'dataset')
        self.set_sample_dimension = self.sizes(self,'sample')
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
        usable_w = self.dataset_dimension[0] - hor_margin
        ver_margin = self.margin_top_mm + self.margin_bottom_mm
        usable_h = self.dataset_dimension[1] - ver_margin
        hspace_smpl_require = self.samples_dimensions[0]+self.minh_spacing_mm
        vspace_smpl_require = self.samples_dimensions[1]+self.minh_spacing_mm
        #Actually we have to consider that the last sample can be place next to
        # the margin, so we add the spacing to the effective space
        effective_hspace = usable_w+self.minh_spacing_mm
        print(effective_hspace)
        print(hspace_smpl_require)
        samples_per_row = int(effective_hspace/hspace_smpl_require)
        print(samples_per_row)
        effective_vspace = usable_h + self.minv_spacing_mm
        max_number_of_rows = int(effective_vspace/vspace_smpl_require)
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
        x,y,_ = self.dataset_dimension
        #Top left
        utl = draw_mtf_aligment(xcenter=spacing, ycenter=spacing,r=r)
        #Top right
        utr = draw_mtf_aligment(xcenter= x - spacing, ycenter=spacing,r=r)
        #Bottom left
        btl = draw_mtf_aligment(xcenter=spacing, ycenter= y - spacing,r=r)
        #Bottom right
        btr = draw_mtf_aligment(xcenter= x - spacing, ycenter= y - spacing,r=r)
        self._alignment_MTF_standards = utl + utr + btl + btr


    def populate_with_samples(self,material,process='?',thickness='?'):
        '''
        Add sample instance to the dataset.
        '''
        width,height,thickness = self.samples_dimensions
        if width is str or height is str:
            ValueError("Sample size haven't been set or are incorrect!")
        for i in range(self.number_of_samples):
            s = Sample(width = width,
                       height = height,
                       material = material,
                       process = process,
                       thickness = thickness)
            self.samples.append(s)

    def add_sample(self,material,process='?'):
        '''
        Add sample instance to the dataset.
        '''
        width,height,thickness = self.samples_dimensions
        if width is str or height is str:
            ValueError("Sample size haven't been set or are incorrect!")
        s = Sample(width = width,
                   height = height,
                   material = material,
                   process = process,
                   thickness = thickness)
        self.samples.append(s)
        return s
    
    def set_dataset_dimension(self):
        pass
    
    def set_sample_dimension(self):
        pass

    def save_svg(self,border_as_cutline = True):
        if self._samples_ID == []:
            self._samples_ID = range(self.number_of_samples)
        with open('%s.svg' %self.name,'w') as f:
            x,y,_ = self.dataset_dimension
            w,h,_ = self.samples_dimensions
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
            f.write( r"""<g id="samples_position">"""+"\n" )
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
            
            if self.samples != []:
                f.write( r"""<g id="samples">"""+"\n" )
                for index, coord in enumerate(self._samples_coordinates):
                    ids = self._samples_ID[index]
                    sample = self.samples[index]
                    for element in sample.elements.values():
                        if element['kind'] == 'layer':
                            f.write( r"""   <rect
      x="%s"
      y="%s"
      id="%s"
      width="%s"
      height="%s"
      stroke="yellow"
      stroke-width="0.2"
      stroke-opacity="0.2"
      fill-opacity="0.3" /> """ %(coord[0] + element['xi'],
                                  coord[1] + element['yi'],
                                  ids,
                                  element['xf']-element['xi'],
                                  element['yf']-element['yi'])+"\n")
                        if element['kind'] == 'treatment':
                           f.write( r"""   <rect
      x="%s"
      y="%s"
      id="%s"
      width="%s"
      height="%s"
      stroke="magenta"
      stroke-opacity="0.2"
      stroke-width="0.5"
      fill="magenta"
      fill-opacity="0.2" /> """ %(coord[0] + element['xi'],
                                  coord[1] + element['yi'],
                                  ids,
                                  element['xf']-element['xi'],
                                  element['yf']-element['yi'])+"\n")
                
                f.write(r"</g>")
                
            if self._alignment_MTF_standards != []:
                f.write(r"""<g id = "MTF" stroke="none" fill="blue">"""+"\n")
                for i in self._alignment_MTF_standards:
                    f.write(i+"\n")
                f.write(r"</g>")

            #Close the file
            f.write(r"</svg>")


if __name__ == '__main__':
    h = Dataset()
    h.name = 'Test2'
    #h.data_set_dimension = s.hMicroscope_slide_petro
#    h.margin_top_mm = 2
#    h.margin_bottom_mm = 2
#    h.margin_left_mm = 2
#    h.margin_right_mm = 2
#    h.samples_dimensions = [5,5,0]
    h.number_of_samples = 12
    h.find_cols_rows()
    #h.cols, h.rows = 1,1
    h.findcord()
    h.populate_with_samples('bronze')
    for sample in h.samples[1:5]:
        sample.add_layer("varnish", "brush", width_percent=0.7)
    for sample in h.samples:
        sample.add_treatment("caleaning", "acetone",width_percent=0.5)
    h.insert_alignment_MTF_standard()
    h.save_svg()


## for sample in dataset.samples[0:5]:
#       sample.add_layer(description = "varnish", ends = (half,half))
#       sample.add_treatment(description = "laser cleaning", params = {"watt":100, "time (sec): 3}, xyorigin = (10,10) xyend = (50,50))

    # Prit masks
