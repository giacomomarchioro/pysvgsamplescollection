# a collection
from svgsamplescollection import SamplesCollection
mySampCol = SamplesCollection()
mySampCol.name = 'Test silver'
mySampCol.set_samplesholder_dimension.A4()
mySampCol.set_sample_dimension.Microscope_slide()
mySampCol.set_number_of_samples(15)
mySampCol.margin_top_mm = 5
mySampCol.margin_bottom_mm = 5
mySampCol.minh_spacing_mm = 10
mySampCol.minv_spacing_mm = 5
mySampCol.create_sample_holder()
mySampCol.populate_with_samples(material='silver')
for sample in mySampCol.samples[1:8]:
    sample.add_treatment("cheased", "graver")
for sample in mySampCol.samples[1:5]:
    sample.add_layer("varnish", "nitorcellulose lacquer", width_percent=0.7)
for sample in mySampCol.samples:
    sample.add_treatment("cleaning", "acetone",width_percent=0.5)
mySampCol.insert_alignment_MTF_standard()
mySampCol.insert_scalebar()
mySampCol.insert_standard()
# Start example
import ezdxf

# 0,0 is bottom left while in svg is top left

y = 220
x = 300

doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
# set units to millilmters
doc.header['$INSUNITS'] = 4
doc.layers.new(name='Sample holder', dxfattribs={'color': 1})
doc.layers.new(name='Text', dxfattribs={'color': 5})
msp = doc.modelspace()  # add new entities to the modelspace

# border line
points = [(0, 0), (x, 0), (x, y), (0, y),(0,0)]
msp.add_lwpolyline(points, dxfattribs={'layer': 'Sample holder'})

ytext = y + mySampCol._title_offset - mySampCol.margin_top_mm
msp.add_text("%s" %mySampCol.name,
             dxfattribs={
                 'layer':'Text',
                 'height': mySampCol.title_font_size_mm}
             ).set_pos((mySampCol.margin_left_mm,ytext ), align='LEFT')
# samples 
if mySampCol._samples_ID == []:
    mySampCol._samples_ID = range(mySampCol.number_of_samples)

w, h, _ = mySampCol.sample_dimension

for index, i in enumerate(mySampCol._samples_coordinates):
                ids = mySampCol._samples_ID[index]
                points = [(i[0], y - i[1]),
                          (i[0]+w, y - i[1]),
                          (i[0]+w, y - i[1] - h),
                          (i[0], y - i[1] - h),
                          (i[0], y - i[1])]
                msp.add_lwpolyline(points, dxfattribs={'layer': 'Sample holder'})

                msp.add_text("ID: %s" %ids,
             dxfattribs={
                 'layer':'Text',
                 'height': mySampCol.label_font_size_mm}
             ).set_pos((i[0], y + mySampCol.text_y - i[1]), align='LEFT')
    #             f.write( r"""   <rect
    #   x="%s"
    #   y="%s"
    #   id="%s"
    #   width="%s"
    #   height="%s"
    #   stroke="red"
    #   stroke-width="0.5"
    #   fill-opacity="0" /> """ %(i[0],i[1],ids,w,h)+"\n")
    #             ty = i[1] - self.text_y

    #             f.write( r"""   <text
    #   x="%s"
    #   y="%s"
    #   font-family="Verdana"
    #   font-size="5"
    #   fill="blue" >
    #   ID: %s  </text>""" %(i[0],ty,ids)+"\n")
    #         f.write( r"</g>"+"\n" )

doc.saveas('line.dxf')