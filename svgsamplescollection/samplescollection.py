'''
Main module for creating a dataset and saving it in svg format.
'''
from .circle_sector import draw_mtf_aligment
from .scalebar import scalebar
from .sample import Sample
import math
import xml.etree.ElementTree as ET
from datetime import datetime
import json

class SamplesCollection:
    """
    The Samplescollection class reppresent the Samplescollection itself.

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
        self.margin_top_mm = 10
        self.margin_bottom_mm = 10
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
        self.date = str(datetime.now())
        self.creators = []
        self.steps = {}
        self.current_step = 0
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
        vspace_smpl_require = self.sample_dimension[1]+self.minv_spacing_mm
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

        effective_vspace = usable_h + self.minv_spacing_mm - self.margin_top_mm - self.margin_bottom_mm
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
        self._alignment_MTF_standards = [utl, utr, btl, btr]

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
        Insert a standard on the left marign.
        """
        x, y, _ = self.dataset_dimension
        if shape == 'circle':
            if yi is None:
                yi = y/2.
            if xi is None:
                xi =  self.margin_left_mm/2.
            if radius is None:
                radius = self.margin_left_mm/3.
            mst = {"shape":shape,
                   "xi":xi,
                   "yi":yi,
                   "radius":radius,
                   "id":len(self._standards),
                   "title":{"name":name,
                   "description":description},
                   "mode":mode}
            self._standards.append(mst)

        if shape == 'rect':
            if yi is None:
                yi = y/2.
            if xi is None:
                xi = self.margin_left_mm/3
            if width is None:
                width = self.margin_left_mm/3.
            if height is None:
                height = y/10

            mst = {
                "shape":shape,
                "xi":xi,
                "yi":yi,
                "id":len(self._standards),
                "width":width,
                "height":height,
                "title":{"name":name,
                "description":description},
                "mode":mode}
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
    
    def add_step(self,description):
        self.current_step +=1
        self.steps[self.current_step] = {"description": description,
                "status":"?",
                "date":"?"}
        for sample in self.samples:
            sample.steps[self.current_step] = description
            sample.current_step = self.current_step
        
    
    def set_number_of_samples(self, number):
        self.number_of_samples = number


    def save_dxf(self, border_as_cutline=True,name=None,positioner=False,positioner_margin=10):
        if name is None:
            name = self.name
        import ezdxf
        # 0,0 is bottom left while in svg is top left
        x,y,_ = self.dataset_dimension
        doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
        # set units to millilmters
        doc.header['$INSUNITS'] = 4
        doc.layers.new(name='Sample holder', dxfattribs={'color': 1})
        doc.layers.new(name='Text', dxfattribs={'color': 5})
        msp = doc.modelspace()  # add new entities to the modelspace

        # border line
        points = [(0, 0), (x, 0), (x, y), (0, y),(0,0)]
        msp.add_lwpolyline(points, dxfattribs={'layer': 'Sample holder'})

        ytext = y + self._title_offset - self.margin_top_mm
        msp.add_text("%s" %self.name,
                    dxfattribs={
                        'layer':'Text',
                        'height': self.title_font_size_mm}
                    ).set_pos((self.margin_left_mm,ytext ), align='LEFT')
        if positioner and border_as_cutline:
            doc.layers.new(name='positioner', dxfattribs={'color': 1})
            points = [(0 - positioner_margin, 0 - positioner_margin),
                      (x + positioner_margin, 0 - positioner_margin),
                      (x + positioner_margin, y + positioner_margin),
                      (0 - positioner_margin, y + positioner_margin),
                      (0 - positioner_margin, 0 - positioner_margin)]
            msp.add_lwpolyline(points, dxfattribs={'layer': 'positioner'})

        # samples 
        if self._samples_ID == []:
            self._samples_ID = range(self.number_of_samples)

        w, h, _ = self.sample_dimension

        for index, i in enumerate(self._samples_coordinates):
                        ids = self._samples_ID[index]
                        points = [(i[0], y - i[1]),
                                (i[0]+w, y - i[1]),
                                (i[0]+w, y - i[1] - h),
                                (i[0], y - i[1] - h),
                                (i[0], y - i[1])]
                        msp.add_lwpolyline(points, dxfattribs={'layer': 'Sample holder'})

                        msp.add_text("ID: %s" %ids,
                    dxfattribs={
                        'layer':'Text',
                        'height': self.label_font_size_mm}
                    ).set_pos((i[0], y + self.text_y - i[1]), align='LEFT')


        if self._alignment_MTF_standards != []:
                        doc.layers.new(name='MTF', dxfattribs={'color': 5})
                        for i in self._alignment_MTF_standards:
                            #[utl, utr, btl, btr]
                            a,b = i
                            ac = ((a['xendpoint'] - a['xstartpoint'])**2 + (a['yendpoint'] - a['ystartpoint'])**2)**0.5
                            sa = a['r'] - (a['r']**2 - (ac/2)**2)**0.5
                            binge_a = sa/(ac/2)
                            apoints = [(a['xcenter'],y - a['ycenter'],0),
                                    (a['xstartpoint'],y - a['ystartpoint'],binge_a),
                                    (a['xendpoint'], y - a['yendpoint'],0),
                                    (a['xcenter'],y - a['ycenter'],0),]
                            lwpolylinea = msp.add_lwpolyline(apoints,format='xyb', 
                            dxfattribs={'layer':'MTF'})
                            bc = ((b['xendpoint'] - b['xstartpoint'])**2 + (b['yendpoint'] - b['ystartpoint'])**2)**0.5
                            sb = b['r'] - (b['r']**2 - (bc/2)**2)**0.5
                            binge_b = sb/(bc/2)
                            bpoints = [(b['xcenter'],y - b['ycenter'],0),
                                    (b['xstartpoint'], y - b['ystartpoint'],binge_b),
                                    (b['xendpoint'],y - b['yendpoint'],0),
                                    (b['xcenter'],y - b['ycenter'],0),]
                            lwpolylineb = msp.add_lwpolyline(bpoints,format='xyb',dxfattribs={'layer':'MTF'})

                            hatch = msp.add_hatch(color=5)
                            path = hatch.paths.add_polyline_path(
                            # get path vertices from associated LWPOLYLINE entity
                            lwpolylinea.get_points(format='xyb'),
                            # get closed state also from associated LWPOLYLINE entity
                            is_closed=lwpolylinea.closed,)
                            path = hatch.paths.add_polyline_path(
                            # get path vertices from associated LWPOLYLINE entity
                            lwpolylineb.get_points(format='xyb'),
                            # get closed state also from associated LWPOLYLINE entity
                            is_closed=lwpolylineb.closed,)
                            # We finally add a circle
                            msp.add_circle(center=(a['xcenter'],a['ycenter']),radius=a['r'],dxfattribs={'layer':'MTF'})

        if self._scalebar != []:
            doc.layers.new(name='scalebar', dxfattribs={'color': 5})
            rectangles,texts = self._scalebar
            for i in rectangles:
                points = [(i[0], y - i[1]),
                                    (i[0]+i[2], y - i[1]),
                                    (i[0]+i[2], y - i[1] - i[3]),
                                    (i[0], y - i[1] - i[3]),
                                    (i[0], y - i[1])]
                lwpolyliner = msp.add_lwpolyline(points, 
                            dxfattribs={'layer':'scalebar'})
                hatch = msp.add_hatch(color=5)
                path = hatch.paths.add_polyline_path(
                # get path vertices from associated LWPOLYLINE entity
                lwpolyliner.get_points(format='xy'),
                # get closed state also from associated LWPOLYLINE entity
                is_closed=lwpolyliner.closed,)
            for j in texts:
                align = 'CENTER'
                if j[-1] == 'mm':
                    align = 'LEFT'
                msp.add_text(str(j[3]),
                    dxfattribs={
                        'layer':'Text',
                        'height': str(j[2])}
                    ).set_pos((j[0], y - j[1]), align=align)

        if self._standards != []:
            doc.layers.new(name='standards', dxfattribs={'color': 1})
            for i in self._standards:
                if i["shape"] == "rect":
                    points = [(i["xi"], y - i["yi"]),
                                        (i["xi"]+i["width"], y - i["yi"]),
                                        (i["xi"]+i["width"], y - i["height"]- i["yi"]),
                                        (i["xi"], y - i["height"] - i["yi"]),
                                        (i["xi"], y - i["yi"])]
                    lwpolyliner = msp.add_lwpolyline(points, 
                                dxfattribs={'layer':'standards'})
                if i["shape"] == "circle":
                    msp.add_circle(center=(i['xi'],i['yi']),radius=i['radius'],dxfattribs={'layer':'standards'})

        doc.saveas('%s.dxf' %self.name)
    

    def save_masks_dxf(self,border_as_cutline=True,labels=True,name=None):
        import ezdxf
        if name is None:
            name = self.name
        # samples 
        if self._samples_ID == []:
            self._samples_ID = range(self.number_of_samples)

        w, h, _ = self.sample_dimension
        x,y,_ = self.dataset_dimension
        # for each step we save a mask
        for idx in range(1,self.current_step+1):       
            # 0,0 is bottom left while in svg is top left
            
            doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
            # set units to millilmters
            doc.header['$INSUNITS'] = 4
            doc.layers.new(name='Sample holder', dxfattribs={'color': 1})
            doc.layers.new(name='Text', dxfattribs={'color': 5})
            msp = doc.modelspace()  # add new entities to the modelspace

            # border line
            points = [(0, 0), (x, 0), (x, y), (0, y),(0,0)]
            msp.add_lwpolyline(points, dxfattribs={'layer': 'Sample holder'})

            ytext = y + self._title_offset - self.margin_top_mm
            msp.add_text("%s step %s" %(self.name,idx),
                        dxfattribs={
                            'layer':'Text',
                            'height': self.title_font_size_mm}
                        ).set_pos((self.margin_left_mm,ytext ), align='LEFT')
            for index, coord in enumerate(self._samples_coordinates):
                # xi and yi are relative to the sample coordiantes
                ids = self._samples_ID[index]
                sample = self.samples[index]
                for element in sample.elements.values():
                    if element['info']['step'] == idx:
                        points = [(coord[0], y - coord[1]),
                                (coord[0]+w, y - coord[1]),
                                (coord[0]+w, y - coord[1] - h),
                                (coord[0], y - coord[1] - h),
                                (coord[0], y - coord[1])]
                        msp.add_lwpolyline(points, dxfattribs={'layer': 'Sample holder'})
                        if labels:
                            tick = ''
                            if 'material' in element['info'].keys():
                                var = element['info']['material']
                                tick = element['info']['thickness_microns']
                                tick = ", %s um" %tick
                            else:
                                var = element['info']['parameters']
                            proc = element['info']['process']
                            msp.add_text("%s, %s%s" %(proc,var,tick),
                            dxfattribs={
                                'layer':'Text',
                                'height': self.label_font_size_mm}
                            ).set_pos((coord[0], y + self.text_y - coord[1]), align='LEFT')
            doc.saveas('mask_step%s.dxf' %idx)
                           
                            


    def _save_tree(self,p,name):
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
            return True

    def _create_svgheader(self, border_as_cutline=True, save_samples=True, name=None,positioner=False,positioner_margin=10):
        if name == None:
            name = self.name
        x, y, _ = self.dataset_dimension
        w, h, _ = self.sample_dimension
        p = ET.Element('svg')
        p.set("version", "1.1")
        p.set("baseProfile", "full")
        if positioner and not save_samples and border_as_cutline:
            p.set("width","%smm"%(x+positioner_margin*2))
            p.set("height","%smm"%(y+positioner_margin*2))
            p.set("viewBox","%s %s %s %s"%(-positioner_margin,
                                           -positioner_margin,
                                           x+positioner_margin*2,
                                           y+positioner_margin*2))
        else:
            p.set("width","%smm"%x)
            p.set("height","%smm"%y)
            p.set("viewBox","0 0 %s %s"%(x,y))
        p.set("xmlns","http://www.w3.org/2000/svg")
        main_title = ET.SubElement(p, 'title')
        main_title.text = name
        # https://www.w3.org/TR/SVG11/metadata.html
        metadata = ET.SubElement(p,'metadata')
        rdf = ET.SubElement(metadata,'rdf:RDF')
        rdf.set('xmlns:rdf',"http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        rdf.set('xmlns:rdfs',"http://www.w3.org/2000/01/rdf-schema#")
        rdf.set('xmlns:dc',"http://purl.org/dc/elements/1.1/")
        desc = ET.SubElement(rdf,'rdf:Description')
        if self.about is not None:
            desc.set('about',self.about)
        if name is not None:
            desc.set('dc:title',name)
        if self.description is not None:
            desc.set('dc:description',self.description)
        if self.publisher is not None:
            desc.set('dc:publisher',self.publisher)
        desc.set('dc:date',self.date)
        desc.set('dc:format',"image/svg+xml")
        desc.set('dc:language',"en")
        creator = ET.SubElement(desc,'dc:creator')
        bag = ET.SubElement(creator,'rdf:Bag')
        for i in self.creators:
            c = ET.SubElement(bag,'rdf:li')
            c.text = i
        ytit = self.margin_top_mm - self._title_offset
        xtit = self.margin_left_mm
        # Image
        img = ET.SubElement(p, 'image')
        img.set("id","backgroundimage")
        # Title
        title_e = ET.SubElement(p, 'text')
        title_e.set("x",str(xtit))
        title_e.set("y",str(ytit))
        title_e.set("font-family","Verdana")
        title_e.set("font-size",str(self.title_font_size_mm))
        title_e.set("fill","blue")
        title_e.text = name
        border_e = ET.SubElement(p,'rect')
        border_e.set("x","0")
        border_e.set("y","0")
        border_e.set("id","collection_border")
        border_e.set("width",str(x))
        border_e.set("height",str(y))
        border_e.set("stroke-width","1")
        border_e.set("fill-opacity","0")
        if border_as_cutline:
            border_e.set("stroke","red")
        else:
            border_e.set("stroke","blue")
        tx = ET.SubElement(border_e, 'title')
        tx.text = json.dumps(self.steps,indent=1)
        if positioner and not save_samples and border_as_cutline:
            pos = ET.SubElement(p, 'rect')
            pos.set("x",str(0 - positioner_margin))
            pos.set("y",str(0 - positioner_margin))
            pos.set("id","positioner")
            pos.set("width",str(x + positioner_margin*2))
            pos.set("height",str(y + positioner_margin*2))
            pos.set("stroke","red")
            pos.set("stroke-width","0.5")
            pos.set("fill-opacity","0")
        return p

    def save_svg(self, border_as_cutline=True, save_samples=True, name=None,positioner=False,positioner_margin=10):
        if self._samples_ID == []:
            self._samples_ID = range(self.number_of_samples)
        if name is None:
            name = self.name
        x, y, _ = self.dataset_dimension
        w, h, _ = self.sample_dimension
        # create svg header and get root of xml file
        p = self._create_svgheader(border_as_cutline=border_as_cutline,name=name,
                                   save_samples=save_samples,positioner=positioner,
                                   positioner_margin=positioner_margin)
        # we add the sample position
        sem_pos = ET.SubElement(p, 'g')
        sem_pos.set("id","samples_position")
        for index, i in enumerate(self._samples_coordinates):
            ids = self._samples_ID[index]
            se = ET.SubElement(sem_pos, 'rect')
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
            tite.set("fill","blue")
            tite.text = "ID: %s" %ids
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
                        t.text = json.dumps(element['info'],indent=1)
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
                        s.set("fill","magenta")
                        t = ET.SubElement(s, 'title')
                        t.text = json.dumps(element['info'],indent=1)

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
            for ind,t in enumerate(texts):
                te = ET.SubElement(sbs,'text')
                te.set("x",str(t[0]))
                te.set("y",str(t[1]))
                te.set("font-family","Verdana")
                if ind != len(texts)-1:
                    te.set("text-anchor","middle")
                te.set("font-size",str(t[2]))
                te.text = str(t[3])
        
        if self._alignment_MTF_standards != []:
            mtf = ET.SubElement(p,'g')
            mtf.set("id","MTF")
            mtf.set("stroke","none")
            mtf.set("fill","blue")
            for i in self._alignment_MTF_standards:
                #[utl, utr, btl, btr]
                amtf = ET.SubElement(mtf,'g')
                a,b = i
                path_a = ET.SubElement(amtf,'path')
                ta = " M %s %s A %s %s 0 %s 0 %s %s  L %s %s Z" %(
                a['xstartpoint'],a['ystartpoint'],
                a['r'],a['r'],
                a['large_arc_flag'],
                a['xendpoint'],a['yendpoint'],
                a['xcenter'], a['ycenter'],)
                path_a.set('d',ta)
                path_b = ET.SubElement(amtf,'path')
                tb = " M %s %s A %s %s 0 %s 0 %s %s  L %s %s Z" %(
                b['xstartpoint'],b['ystartpoint'],
                b['r'],b['r'],
                b['large_arc_flag'],
                b['xendpoint'],b['yendpoint'],
                b['xcenter'], b['ycenter'],)
                path_b.set('d',tb)
                circle = ET.SubElement(amtf,'circle')
                circle.set("cx",str(a['xcenter']))  
                circle.set("cy",str(a['ycenter']))  
                circle.set("r",str(a['r']))  
                circle.set("stroke","blue")  
                circle.set("stroke-width","0.5")
                circle.set("fill","none")    

        if self._standards != []:
            std = ET.SubElement(p,'g')
            std.set("id","standards")
            std.set("stroke","none")
            mode = {'cut':'red'}
            for i in self._standards:
                if i['shape'] == 'circle':
                    cir = ET.SubElement(std,'circle')
                    cir.set("cx",str(i['cx']))
                    cir.set("cy",str(i['cy']))
                    cir.set("r",str(i['r']))
                    cir.set("id",str(i['id']))
                    cir.set("stroke",mode[i['mode']])
                    T = ET.SubElement(std,'title')
                    T.text = json.dumps(i['title'],indent=1)
                if i['shape'] == 'rect':
                    rect = ET.SubElement(std,'rect')
                    rect.set("x",str(i['xi']))
                    rect.set("y",str(i['yi']))
                    rect.set("id",str(i['id']))
                    rect.set("stroke",mode[i['mode']])
                    rect.set("width",str(i['width']))
                    rect.set("height",str(i['height']))
                    rect.set("stroke-width","0.5")
                    rect.set("fill-opacity","0")
                    T = ET.SubElement(std,'title')
                    T.text = json.dumps(i['title'],indent=1)
        if not save_samples:
            name = "sampleholder_%s" %name
        self._save_tree(p,name)
        
    def save_masks_svg(self,border_as_cutline=True,labels=True,positioner=False,positioner_margin=10):

        # This saves only the sample holder
        self.save_svg(border_as_cutline=True, save_samples=False,
                      name = None,positioner=positioner,
                      positioner_margin=positioner_margin)
        # for each step we save a mask
        for idx in range(1,self.current_step+1):
            name = "mask step %s" %idx
            p = self._create_svgheader(border_as_cutline=border_as_cutline,name=name)
            sems= ET.SubElement(p, 'g')
            sems.set("id","layers")
            for index, coord in enumerate(self._samples_coordinates):
                # xi and yi are relative to the sample coordiantes
                ids = self._samples_ID[index]
                sample = self.samples[index]
                for element in sample.elements.values():
                    if element['info']['step'] == idx:
                        s = ET.SubElement(sems, 'rect')
                        s.set("x",str(coord[0] + element['xi']))
                        s.set("y",str(coord[1] + element['yi']))
                        s.set("id",str(ids))
                        s.set("width",str(element['xf']-element['xi']))
                        s.set("height",str(element['yf']-element['yi']))
                        s.set("stroke","red")
                        s.set("stroke","red")
                        s.set("stroke-width","0.5")
                        s.set("fill-opacity","0")
                        t = ET.SubElement(s, 'title')
                        t.text = json.dumps(element['info'],indent=1)
                        ty = coord[1] - self.text_y
                        if labels:
                            tite = ET.SubElement(p, 'text')
                            tite.set("x",str(coord[0]))
                            tite.set("y",str(ty))
                            tite.set("font-family","Verdana")
                            tite.set("font-size",str(self.label_font_size_mm))
                            tite.set("fill","blue")
                            tick = ''
                            if 'material' in element['info'].keys():
                                var = element['info']['material']
                                tick = element['info']['thickness_microns']
                                tick = ", %s um" %tick
                            else:
                                var = element['info']['parameters']
                            proc = element['info']['process']
                            tite.text = "%s, %s%s" %(proc,var,tick)
            self._save_tree(p,name)


    def nosteps_save_masks_svg(self,border_as_cutline=True):
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

    