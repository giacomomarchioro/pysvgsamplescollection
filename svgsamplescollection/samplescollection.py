'''
Main module for creating a dataset and saving it in svg format.
'''
from circle_sector import draw_mtf_aligment
from scalebar import scalebar
from sample import Sample
import math


class Samplescollection:
    """
    The Samplescollection class rappresent the Samplescollection itself.

    It contains the methods for adding the samples and saving them to the svg
    file.
    """

    class sizes:
        """
        Standard sizes.

        This class is used for facilitating the setting of the sizes of the
        dataset element.
        """

        def __init__(self, d, kind):
            """Use for convinence."""
            self._d = d
            self._kind = kind

        def _assign(self, dim, kind):
            if kind == 'dataset':
                self._d.dataset_dimension = dim
            if kind == 'sample':
                self._d.sample_dimension = dim

        def vMicroscope_slide(self):
            self._assign([25, 70, 1], self._kind)

        def vMicroscope_slide_geo(self):
            self._assign([50, 75, 1], self._kind)

        def vMicroscope_slide_petro(self):
            self._assign([27, 46, 1], self._kind)

        def vA7(self):
            self._assign([81, 114, 0], self._kind)

        def vA4(self):
           self._assign([210, 297, 0], self._kind)

        def Microscope_slide(self):
           self._assign([ 70, 25, 1], self._kind)

        def Microscope_slide_geo(self):
           self._assign([75, 50, 1], self._kind)

        def Microscope_slide_petro(self):
           self._assign([46, 27, 1], self._kind)

        def A7(self):
           self._assign([ 114, 81, 0], self._kind)

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
        self._scalebar = []
        self._standards = []

    def create_sample_holder(self):
        '''
        This method find the max number of samples that can be fit in the
        dataset.
        '''
        num_samples = self.number_of_samples
        hor_margin = self.margin_left_mm + self.margin_right_mm
        usable_w = self.dataset_dimension[0] - hor_margin
        ver_margin = self.margin_top_mm + self.margin_bottom_mm
        usable_h = self.dataset_dimension[1] - ver_margin
        hspace_smpl_require = self.sample_dimension[0]+self.minh_spacing_mm
        vspace_smpl_require = self.sample_dimension[1]+self.minh_spacing_mm
        #Actually we have to consider that the last sample can be place next to
        # the margin, so we add the spacing to the effective space
        effective_hspace = usable_w+self.minh_spacing_mm
        print(effective_hspace)
        print(hspace_smpl_require)
        samples_per_row = int(effective_hspace/hspace_smpl_require)
        print(samples_per_row)
        effective_vspace = usable_h + self.minv_spacing_mm
        max_number_of_rows = int(effective_vspace/vspace_smpl_require)
        print('maxnumber', max_number_of_rows)
        if samples_per_row*max_number_of_rows >= num_samples:
            self.rows = int(math.ceil(num_samples/float(samples_per_row)))
            self.cols = samples_per_row
        else:
            print("Max number of samples: %s" %(samples_per_row*max_number_of_rows))
            print("Too many samples! Try to decrese margins or spacing!")
            return False

        xlen = self.sample_dimension[0]+self.minh_spacing_mm
        xs = [self.margin_left_mm + xlen*i for i in range(self.cols) ]
        ylen = self.sample_dimension[1]+self.minv_spacing_mm
        ys = [self.margin_top_mm + ylen*i for i in range(self.rows) ]
        counter = 0
        # Now we find the sample coordinates in the space
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
        # Top left
        utl = draw_mtf_aligment(xcenter=spacing, ycenter=spacing,r=r)
        # Top right
        utr = draw_mtf_aligment(xcenter= x - spacing, ycenter=spacing,r=r)
        # Bottom left
        btl = draw_mtf_aligment(xcenter=spacing,ycenter= y - spacing,r=r)
        # Bottom right
        btr = draw_mtf_aligment(xcenter= x - spacing, ycenter= y - spacing,r=r)
        self._alignment_MTF_standards = utl + utr + btl + btr

    def insert_scalebar(self):
        x, y, _ = self.dataset_dimension
        height = self.margin_bottom_mm/3.
        yi = y - self.margin_bottom_mm/3.*2
        element_number = 4
        if y/10. > 10:
            element_lenght = 10
        elif y/5. > 10:
            element_lenght = 5
        else:
            element_lenght = 1
        lenght = element_lenght*element_number
        xi = x/2. - lenght/2
        self._scalebar = scalebar(xi=xi,
                                  yi=yi,
                                  height=height,
                                  lenght=None,
                                  element_lenght=element_lenght,
                                  element_number=element_number)

    def insert_standard(self,
                        shape='rect',
                        name='standard',
                        description=None,
                        mode='cut',
                        xi=None,
                        yi=None,
                        height=None,
                        width=None,
                        radius=None):
        """
        Insert a standard on the right marign.
        """
        x, y, _ = self.dataset_dimension
        if shape == 'circle':
            if yi is None:
                yi = y/2.
            if xi is None:
                xi = x - self.margin_right_mm/2.
            if radius is None:
                radius = self.margin_right_mm/3.
            mst = """<circle cx="%s" cy="%s" r="%s">
            <title>name: %s
            description: %s
            </title>
            </circle>""" % (xi,
                            yi,
                            radius,
                            name,
                            description)
            self._standards.append(mst)

        if shape == 'rect':
            if yi is None:
                yi = y/2.
            if xi is None:
                xi = x - self.margin_right_mm/3.*2
            if width is None:
                width = self.margin_right_mm/3.
            if height is None:
                height = y/10

            mst = """<rect
            x="%s"
            y="%s"
            id="%s"
            width="%s"
            height="%s"
            stroke="red"
            stroke-width="0.5"
            fill-opacity="0">
            <title>name: %s
            description: %s
            </title>
            </rect>""" % (xi,
                          yi,
                          len(self._standards),
                          width,
                          height,
                          name,
                          description)
            self._standards.append(mst)

    def populate_with_samples(self, material, process='?', thickness='?'):
        '''
        Add sample instance to the dataset.
        '''
        width, height, thickness = self.sample_dimension
        if width is str or height is str:
            ValueError("Sample size haven't been set or are incorrect!")
        for i in range(self.number_of_samples):
            s = Sample(width=width,
                       height=height,
                       material=material,
                       process=process,
                       thickness=thickness)
            self.samples.append(s)

    def add_sample(self, material, process='?'):
        '''
        Add sample instance to the dataset.
        '''
        width, height, thickness = self.sample_dimension
        if width is str or height is str:
            ValueError("Sample size haven't been set or are incorrect!")
        s = Sample(width=width,
                   height=height,
                   material=material,
                   process=process,
                   thickness=thickness)
        self.samples.append(s)
        return s

    def set_number_of_samples(self, number):
        self.number_of_samples = number


    def save_svg(self, border_as_cutline=True, save_samples=True, name=None):
        if self._samples_ID == []:
            self._samples_ID = range(self.number_of_samples)
        if name is None:
            name = self.name
        with open('%s.svg' % name, 'w') as f:
            x, y, _ = self.dataset_dimension
            w, h, _ = self.sample_dimension
            f.write(r"""<svg version="1.1"
   baseProfile="full" width="%smm"
   height="%smm"
   viewBox="0 0 %s %s"
   xmlns="http://www.w3.org/2000/svg">""" %(x,y,x,y) +"\n")
            ytit = self.margin_top_mm/2
            xtit = self.margin_left_mm
            # Collection name
            f.write( r"""<text
   x="%s"
   y="%s"
   id="collection_name"
   font-family="Verdana"
   font-size="10"
   fill="blue">
   %s  </text>"""%(xtit,ytit,self.name)+"\n")

            if border_as_cutline:
                f.write( r"""<rect
   x="0"
   y="0"
   id="collection_border"
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

            if self.samples != [] and save_samples:
                f.write( r"""<g id="samples">"""+"\n" )
                for index, coord in enumerate(self._samples_coordinates):
                    ids = self._samples_ID[index]
                    sample = self.samples[index]
                    for element in sample.elements.values():
                        if element['kind'] == 'layer':
                            f.write(r"""   <rect

      x="%s"
      y="%s"
      id="%s"
      width="%s"
      height="%s"
      stroke="yellow"
      stroke-width="0.4"
      stroke-opacity="0.8"
      fill-opacity="0.3" >
      <title>material: %s
    process: %s</title>
      </rect>
      """ %(
                                  coord[0] + element['xi'],
                                  coord[1] + element['yi'],
                                  ids,
                                  element['xf']-element['xi'],
                                  element['yf']-element['yi'],
                                  element['material'],
                                  element['process'])+"\n")
                        if element['kind'] == 'treatment':
                           f.write( r"""   <rect
      x="%s"
      y="%s"
      id="%s"
      width="%s"
      height="%s"
      stroke="magenta"
      stroke-opacity="0.8"
      stroke-width="0.3"
      fill="magenta"
      fill-opacity="0.2" >
      <title>process: %s
    parameters: %s
    duration: %s</title>
      </rect>      """ %(coord[0] + element['xi'],
                                  coord[1] + element['yi'],
                                  ids,
                                  element['xf']-element['xi'],
                                  element['yf']-element['yi'],
                                  element['process'],
                                  element['parameters'],
                                  element['duration']
                                  )+"\n")

                f.write(r"</g>")

            if self._alignment_MTF_standards != []:
                f.write(r"""<g id = "MTF" stroke="none" fill="blue">"""+"\n")
                for i in self._alignment_MTF_standards:
                    f.write(i+"\n")
                f.write(r"</g>")
            if self._scalebar != []:
                f.write(r"""<g id = "scalebar" stroke="none" fill="blue">"""+"\n")
                for i in self._scalebar:
                    f.write(i+"\n")
                f.write(r"</g>")
            if self._standards != []:
                f.write(r"""<g id = "standards" stroke="none">"""+"\n")
                for i in self._standards:
                    f.write(i+"\n")
                f.write(r"</g>")
            #Close the file
            f.write(r"</svg>")



    def save_masks_svg(self,border_as_cutline=True):
        samx = max([sample._number_of_elements for sample in self.samples])
        # This saves only the sample holder
        self.save_svg(border_as_cutline=True, save_samples=False,name ='sampleholder')
        # These are
        for idc in range(1,samx):
            with open('%s_mask_%s.svg' %(self.name,idc),'w') as f:
                x,y,_ = self.dataset_dimension
                w,h,_ = self.sample_dimension
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
       MASK %s: %s  </text>"""%(xtit,ytit,idc,self.name)+"\n")

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
                for index, coord in enumerate(self._samples_coordinates):
                    ids = self._samples_ID[index]
                    sample = self.samples[index]
                    try:
                        element = sample.elements[idc]
                        if element['kind'] == 'layer':
                                f.write(r"""   <rect
                                          x="%s"
                                          y="%s"
                                          id="%s"
                                          width="%s"
                                          height="%s"
                                          stroke="red"
                                          stroke-width="0.4"
                                          fill-opacity="0.3" >
                                          <title>material: %s process: %s</title>
                                          </rect>
                                          """ %(
                                                  coord[0] + element['xi'],
                                                  coord[1] + element['yi'],
                                                  ids,
                                                  element['xf']-element['xi'],
                                                  element['yf']-element['yi'],
                                                  element['material'],
                                                  element['process'])+"\n")

                                f.write( r"""   <text
                                      x="%s"
                                      y="%s"
                                      font-family="Verdana"
                                      font-size="3"
                                      fill="blue" >
                                      material: %s; process: %s
                                      </text>"""%(coord[0],
                                                  coord[1],
                                                  element['material'],
                                                  element['process'])+"\n")

                        if element['kind'] == 'treatment':
                                   f.write( r"""   <rect
              x="%s"
              y="%s"
              id="%s"
              width="%s"
              height="%s"
              stroke="red"
              stroke-width="0.3"
              fill-opacity="0.2" >
              <title>process: %s parameters: %s duration: %s</title>
              </rect>      """ %(coord[0] + element['xi'],
                                          coord[1] + element['yi'],
                                          ids,
                                          element['xf']-element['xi'],
                                          element['yf']-element['yi'],
                                          element['process'],
                                          element['parameters'],
                                          element['duration']
                                          )+"\n")

                                   f.write( r"""   <text
                                          x="%s"
                                          y="%s"
                                          font-family="Verdana"
                                          font-size="3"
                                          fill="blue" >
                                          process: %s; parameter: %s; duration: %s
                                          </text>""" % (coord[0],
                                                        coord[1],
                                                        element['process'],
                                                        element['parameters'],
                                                        element['duration']) +"\n")
                    except:
                        IndexError

                f.write(r"</g>")
                #Close the file
                f.write(r"</svg>")

if __name__ == '__main__':
    mycollection = Samplescollection()
    mycollection.name = 'Test samples collection'
    mycollection.set_dataset_dimension.A4()
    mycollection.set_sample_dimension.Microscope_slide()
    mycollection.set_number_of_samples(15)
    mycollection.create_sample_holder()
    mycollection.populate_with_samples('wood')
    for sample in mycollection.samples[1:]:
        sample.add_layer("vermilion egg tempera", "brush", width_percent=0.9)
    for sample in mycollection.samples[1:5]:
        sample.add_layer("varnish", "brush", width_percent=0.7)
    for sample in mycollection.samples:
        sample.add_treatment("cleaning", "acetone",width_percent=0.5)
    mycollection.insert_alignment_MTF_standard()
    mycollection.insert_scalebar()
    mycollection.insert_standard()
    mycollection.save_svg()
    mycollection.save_masks_svg()


## for sample in dataset.samples[0:5]:
#       sample.add_layer(description = "varnish", ends = (half,half))
#       sample.add_treatment(description = "laser cleaning", params = {"watt":100, "time (sec): 3}, xyorigin = (10,10) xyend = (50,50))

    # Prit masks
