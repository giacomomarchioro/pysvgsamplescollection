'''
Main module for creating a dataset and saving it in svg format.
'''
from .circle_sector import draw_mtf_aligment
from .scalebar import scalebar
from .sample import Sample
import math
import xml.etree.ElementTree as ET

class SamplesCollection:
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
        self.text_y = None
        self.rows = None
        self.cols = None
        self.minh_spacing_mm = 10
        self.minv_spacing_mm = 10
        self.title_font_size_mm = None
        self.label_font_size = 10
        self.label_font_size_mm = None
        self.set_samplesholder_dimension = self.sizes(self,'dataset')
        self.set_sample_dimension = self.sizes(self,'sample')
        self.publisher = None
        self.about = None
        self.description = None
        self.creators = []
        self._alignment_MTF_standards = []
        self._samples_coordinates = []
        self._samples_ID = []
        self._scalebar = []
        self._standards = []
        self._title_offset = None

    def add_creator(self,name_surname):
        self.creators.append(name_surname)

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
        # Actually we have to consider that the last sample can be place next to
        # the margin, so we add the spacing to the effective space
        effective_hspace = usable_w+self.minh_spacing_mm
        print(effective_hspace)
        print(hspace_smpl_require)
        samples_per_row = int(effective_hspace/hspace_smpl_require)
        print(samples_per_row)
        # on the top of each sample there will be the ID
        # the labels text will be centered between the samples
        self.text_y = self.minv_spacing_mm*0.2
        # the maximum text height for labels is computed
        self.label_font_size_mm = self.minv_spacing_mm - self.text_y*2
        # the maximum text height for title is computed
        self._title_offset = self.margin_top_mm*0.2
        self.title_font_size_mm = self.margin_top_mm - self._title_offset*2

        effective_vspace = usable_h - self.minv_spacing_mm - self.margin_top_mm - self.margin_bottom_mm
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
        ys = [self.margin_top_mm + self.minv_spacing_mm + ylen*i for i in range(self.rows) ]
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
    
    def add_layers(self,ids=None,):
        if ids is None:
            ids = range(self.number_of_samples)
        for i in ids:
            self.samples[i].add_layer()
        
    
    def add_treatments(self,):
        pass
    
    def add_step(self,):
        pass
    
    def set_number_of_samples(self, number):
        self.number_of_samples = number


    def save_dxf(self, border_as_cutline=True, save_samples=True, name=None):
        import ezdxf
        if self._samples_ID == []:
            self._samples_ID = range(self.number_of_samples)
        if name is None:
            name = self.name

        doc = ezdxf.new(dxfversion='R2010')

        # Create new table entries (layers, linetypes, text styles, ...).
        doc.layers.new('TEXTLAYER', dxfattribs={'color': 2})

        # DXF entities (LINE, TEXT, ...) reside in a layout (modelspace, 
        # paperspace layout or block definition).  
        msp = doc.modelspace()

        # Add entities to a layout by factory methods: layout.add_...() 
        msp.add_line((0, 0), (10, 0), dxfattribs={'color': 7})
        msp.add_text(
            'Test', 
            dxfattribs={
                'layer': 'TEXTLAYER'
            }).set_pos((0, 0.2), align='CENTER')
        msp = doc.modelspace()
        doc.layers.new(name='Sample holder', dxfattribs={'color': 1})
        
        # Save DXF document.
        
        x, y, _ = self.dataset_dimension
        w, h, _ = self.sample_dimension
        ytit = self.margin_top_mm/2
        xtit = self.margin_left_mm
        msp.add_text(
            self.name, 
            dxfattribs={
                'layer': 'TEXTLAYER'
            }).set_pos((xtit, ytit), align='CENTER')
            # Collection name


        if border_as_cutline:
            points = [(0, 0), (0, y), (x, 0), (x, y)]
            msp.add_lwpolyline(points)

#                 f.write( r"""<rect
#    x="0"
#    y="0"
#    id="collection_border"
#    width="%s"
#    height="%s"
#    stroke="red"
#    stroke-width="1"
#    fill-opacity="0"  />""" %(x,y)+"\n" )
#             f.write( r"""<g id="samples_position">"""+"\n" )
#             for index, i in enumerate(self._samples_coordinates):
#                 ids = self._samples_ID[index]
#                 f.write( r"""   <rect
#       x="%s"
#       y="%s"
#       id="%s"
#       width="%s"
#       height="%s"
#       stroke="red"
#       stroke-width="0.5"
#       fill-opacity="0" /> """ %(i[0],i[1],ids,w,h)+"\n")
#                 ty = i[1] - self.text_y

#                 f.write( r"""   <text
#       x="%s"
#       y="%s"
#       font-family="Verdana"
#       font-size="5"
#       fill="blue" >
#       ID: %s  </text>""" %(i[0],ty,ids)+"\n")
#             f.write( r"</g>"+"\n" )

#             if self.samples != [] and save_samples:
#                 f.write( r"""<g id="samples">"""+"\n" )
#                 for index, coord in enumerate(self._samples_coordinates):
#                     ids = self._samples_ID[index]
#                     sample = self.samples[index]
#                     for element in sample.elements.values():
#                         if element['kind'] == 'layer':
#                             f.write(r"""   <rect

#       x="%s"
#       y="%s"
#       id="%s"
#       width="%s"
#       height="%s"
#       stroke="yellow"
#       stroke-width="0.4"
#       stroke-opacity="0.8"
#       fill-opacity="0.3" >
#       <title>material: %s
#     process: %s
#     thickness: %s
#     status: %s
#     applied_date: %s 
#     removed_date: %s</title>
#       </rect>
#       """ %(
#                                   coord[0] + element['xi'],
#                                   coord[1] + element['yi'],
#                                   ids,
#                                   element['xf']-element['xi'],
#                                   element['yf']-element['yi'],
#                                   element['material'],
#                                   element['process'],
#                                   element['thickness'],
#                                   element['status'],
#                                   element['applied_date'],
#                                   element['removed_date']
#                                   )+"\n")
#                         if element['kind'] == 'treatment':
#                            f.write( r"""   <rect
#       x="%s"
#       y="%s"
#       id="%s"
#       width="%s"
#       height="%s"
#       stroke="magenta"
#       stroke-opacity="0.8"
#       stroke-width="0.3"
#       fill="magenta"
#       fill-opacity="0.2" >
#       <title>process: %s
#     parameters: %s
#     status: %s
#     applied_date: %s
#     layer: %s
#     </title>
#       </rect>      """ %(coord[0] + element['xi'],
#                                   coord[1] + element['yi'],
#                                   ids,
#                                   element['xf']-element['xi'],
#                                   element['yf']-element['yi'],
#                                   element['process'],
#                                   element['parameters'],
#                                   element['status'],
#                                   element['applied_date'],
#                                   element['layer'],
#                                   )+"\n")

#                 f.write(r"</g>")

#             if self._alignment_MTF_standards != []:
#                 f.write(r"""<g id = "MTF" stroke="none" fill="blue">"""+"\n")
#                 for i in self._alignment_MTF_standards:
#                     f.write(i+"\n")
#                 f.write(r"</g>")
#             if self._scalebar != []:
#                 f.write(r"""<g id = "scalebar" stroke="none" fill="blue">"""+"\n")
#                 for i in self._scalebar:
#                     f.write(i+"\n")
#                 f.write(r"</g>")
#             if self._standards != []:
#                 f.write(r"""<g id = "standards" stroke="none">"""+"\n")
#                 for i in self._standards:
#                     f.write(i+"\n")
#                 f.write(r"</g>")
#             #Close the file
#             f.write(r"</svg>")
        doc.saveas('test.dxf')
  
    def save_svg(self, border_as_cutline=True, save_samples=True, name=None):
        if self._samples_ID == []:
            self._samples_ID = range(self.number_of_samples)
        if name is None:
            name = self.name
        x, y, _ = self.dataset_dimension
        w, h, _ = self.sample_dimension
        p = ET.Element('svg')
        p.set("version", "1.1")
        p.set("baseProfile", "full")
        p.set("width","%smm"%x)
        p.set("height","%smm"%y)
        p.set("viewBox","0 0 %s %s"%(x,y))
        p.set("xmlns","http://www.w3.org/2000/svg")
        # https://www.w3.org/TR/SVG11/metadata.html
        metadata = ET.SubElement(p,'metadata')
        rdf = ET.SubElement(metadata,'rdf:RDF')
        rdf.set('xmlns:rdf',"http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        rdf.set('xmlns:rdfs',"http://www.w3.org/2000/01/rdf-schema#")
        rdf.set('xmlns:dc',"http://purl.org/dc/elements/1.1/")
        desc = ET.SubElement(rdf,'rdf:Description')
        desc.set('about',self.about)
        desc.set('dc:title',self.name)
        desc.set('dc:description',self.description)
        desc.set('dc:publisher',self.publisher)
        desc.set('dc:date',self.date)
        desc.set('dc:format',"image/svg+xml")
        desc.set('dc:language',"en")
        desc.set('about',self.about)
        creator = ET.SubElement(desc,'dc:creator')
        bag = ET.SubElement(creator,'rdf:Bag')
        for i in self.creators:
            c = ET.SubElement(bag,'rdf:li')
            c.text = i
        ytit = self.margin_top_mm - self._title_offset
        xtit = self.margin_left_mm
        title_e = ET.SubElement(p, 'text')
        title_e.set("x",str(xtit))
        title_e.set("y",str(ytit))
        title_e.set("font-family","Verdana")
        title_e.set("font-size",str(self.title_font_size_mm))
        title_e.text = self.name
        if border_as_cutline:
            border_e = ET.SubElement(p,'rect')
            border_e.set("x","0")
            border_e.set("y","0")
            border_e.set("id","collection_border")
            border_e.set("width",str(x))
            border_e.set("height",str(y))
            border_e.set("stroke","red")
            border_e.set("stroke-width","1")
            border_e.set("fill-opacity","0")
        sem_pos = ET.SubElement(p, 'g')
        sem_pos.set("id","samples_position")
        for index, i in enumerate(self._samples_coordinates):
            ids = self._samples_ID[index]
            se = ET.SubElement(sem_pos, 'g')
            se.set("x",str(i[0]))
            se.set("y",str(i[1]))
            se.set("id",str(ids))
            se.set("width",str(w))
            se.set("height",str(h))
            se.set("stroke","red")
            se.set("stroke-width","0.5")
            se.set("fill-opacity","0")
            ty = i[1] - self.text_y
            tite = ET.SubElement(sem_pos, 'text')
            tite.set("x",str(i[0]))
            tite.set("y",str(ty))
            tite.set("font-family","Verdana")
            tite.set("font-size",str(self.label_font_size_mm))
            tite.text = str(ids)
        if self.samples != [] and save_samples:
            sems= ET.SubElement(p, 'g')
            sems.set("id","samples")
            for index, coord in enumerate(self._samples_coordinates):
                ids = self._samples_ID[index]
                sample = self.samples[index]
                for element in sample.elements.values():
                    if element['kind'] == 'layer':
                        s = ET.SubElement(sems, 'rect')
                        s.set("x",str(coord[0] + element['xi']))
                        s.set("y",str(coord[1] + element['yi']))
                        s.set("id",str(ids))
                        s.set("width",str(element['xf']-element['xi']))
                        s.set("height",str(element['yf']-element['yi']))
                        s.set("stroke","yellow")
                        s.set("stroke-width","0.4")
                        s.set("stroke-opacity","0.8")
                        s.set("fill-opacity","0.3")
                        t = ET.SubElement(s, 'title')
                        # TODO: better to use a json dump
                        t.text = """material: %s
                                    process: %s
                                    thickness: %s
                                    status: %s
                                    applied_date: %s 
                                    removed_date: %s"""%(
                                  element['material'],
                                  element['process'],
                                  element['thickness'],
                                  element['status'],
                                  element['applied_date'],
                                  element['removed_date']
                                  )
                    if element['kind'] == 'treatment':
                        s = ET.SubElement(sems, 'rect')
                        s.set("x",str(coord[0] + element['xi']))
                        s.set("y",str(coord[1] + element['yi']))
                        s.set("id",str(ids))
                        s.set("width",str(element['xf']-element['xi']))
                        s.set("height",str(element['yf']-element['yi']))
                        s.set("stroke","magenta")
                        s.set("stroke-width","0.3")
                        s.set("stroke-opacity","0.8")
                        s.set("fill-opacity","0.2")
                        t = ET.SubElement(s, 'title')
                        t.text = """process: %s
                                    parameters: %s
                                    status: %s
                                    applied_date: %s 
                                    layer: %s"""%(
                                  element['process'],
                                  element['parameters'],
                                  element['status'],
                                  element['applied_date'],
                                  element['layer'])

            if self._scalebar != []:
                sbs = ET.SubElement(p,'g')
                sbs.set("id","scalebar")
                sbs.set("stroke","none")
                sbs.set("fill","blue")
                rects, texts = self._scalebar
                for i in rects:
                    r = ET.SubElement(sbs,'rect')
                    r.set("x",str(i[0]))
                    r.set("y",str(i[1]))
                    r.set("width",str(i[2]))
                    r.set("height",str(i[3]))
                    r.set("stroke-width","0")
                    r.set("fill","blue")
                for t in texts:
                    te = ET.SubElement(sbs,'text')
                    te.set("x",str(t[0]))
                    te.set("y",str(t[1]))
                    te.set("font-family","Verdana")
                    te.set("font-size",str(t[2]))
                    te.text = str(t[3])

            # if self._standards != []:
            #     f.write(r"""<g id = "standards" stroke="none">"""+"\n")
            #     for i in self._standards:
            #         f.write(i+"\n")
            #     f.write(r"</g>")
            # #Close the file
            # f.write(r"</svg>")
        def indent(elem, level=0):
            i = "\n" + level*"  "
            j = "\n" + (level-1)*"  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for subelem in elem:
                    indent(subelem, level+1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = j
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = j
            return elem  

        indent(p)
        tree = ET.ElementTree(p)
        if not name.endswith('.svg'):
            name+='.svg'
        tree.write(name)

    def save_masks_svg(self,border_as_cutline=True):
        # TODO: it's actually better to save mask of a single step
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
    mycollection = SamplesCollection()
    mycollection.name = 'Test samples collection'
    mycollection.set_samplesholder_dimension.A4()
    mycollection.set_sample_dimension.Microscope_slide()
    mycollection.set_number_of_samples(15)
    mycollection.create_sample_holder()
    mycollection.populate_with_samples('wood')
    for sample in mycollection.samples[1:]:
        sample.add_layer("vermilion egg tempera", "brush", width_percent=0.9)
    for sample in mycollection.samples[1:5]:
        sample.add_layer("varnish", "brush", width_percent=0.7)
    for sample in mycollection.samples[::2]:
        sample.add_treatment("uv curing", 
                             parameters = {"duration": "5 h",
                                           "wavelength_nm":"290"},
                             height_percent=0.5)
    for sample in mycollection.samples:
        sample.add_treatment("cleaning", "acetone",width_percent=0.5)
    mycollection.insert_alignment_MTF_standard()
    mycollection.insert_scalebar()
    mycollection.insert_standard()
    mycollection.save_svg()
    mycollection.save_masks_svg()

    