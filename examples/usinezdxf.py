# a collection
from svgsamplescollection import SamplesCollection
mySampCol = SamplesCollection()
mySampCol.name = 'Test silver'
mySampCol.set_samplesholder_dimension.A4()
mySampCol.set_sample_dimension.Microscope_slide()
mySampCol.set_number_of_samples(15)
mySampCol.margin_top_mm = 15
mySampCol.margin_bottom_mm = 15
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


x,y,_ = mySampCol.dataset_dimension
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


if mySampCol._alignment_MTF_standards != []:
                doc.layers.new(name='MTF', dxfattribs={'color': 5})
                for i in mySampCol._alignment_MTF_standards:
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
   


doc.saveas('line.dxf')