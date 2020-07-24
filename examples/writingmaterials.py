from svgsamplescollection import SamplesCollection
mySampCol = SamplesCollection()
mySampCol.add_creator('Giacomo Marchioro')
mySampCol.publisher = 'Università di Verona'
mySampCol.name = 'Writing materials A1'
mySampCol.set_samplesholder_dimension.A4()
mySampCol.set_sample_dimension.Microscope_slide()
mySampCol.set_number_of_samples(15)
mySampCol.margin_top_mm = 15
mySampCol.margin_bottom_mm = 15
mySampCol.minh_spacing_mm = 10
mySampCol.minv_spacing_mm = 6
mySampCol.create_sample_holder()
mySampCol.add_step("We use wood as base for our collection, we use a drill for creating holes in the margin of the samples.")
mySampCol.populate_with_samples(material='wood')
mySampCol.add_step("We add parchment,paper and bombacin samples sewing them on the drilled wood.")
for sample in mySampCol.samples[0:6]:
    sample.add_layer(material='parchment',process='sewing')
for sample in mySampCol.samples[6:12]:
    sample.add_layer(material='cellulose paper',process='sewing')
for sample in mySampCol.samples[12:15]:
    sample.add_layer(material='bombacin',process='sewing')
mySampCol.add_step("We add two stripes of gall ink ")
for sample in mySampCol.samples:
    sample.add_layer(material='gall ink',process='drawing',yi=4,yf=6)
    sample.add_layer(material='gall ink',process='drawing',yi=16,yf=18)
mySampCol.add_step("We add two stripes of carbon black ink in arabic gum.")
for sample in mySampCol.samples:
    sample.add_layer(material='carbon black',process='drawing',yi=9,yf=11)
    sample.add_layer(material='carbon black',process='drawing',yi=21,yf=23)
mySampCol.add_step("We scape half of the sample with a knife.")
for sample in mySampCol.samples:
    sample.add_treatment("scraping", "iron blade",width_percent=0.5)
mySampCol.add_step("We expose to UV light the half of each sample.")
parameters = {'duration':'5h',
              'type of lamp': 'Wood lamp',
              'Watt/cm2': '15'}
for sample in mySampCol.samples:
    sample.add_treatment("UV fastning", parameters = parameters,height_percent=0.5)
mySampCol.insert_alignment_MTF_standard()
mySampCol.insert_scalebar()
mySampCol.insert_standard()
# we save the svg file with all the information
mySampCol.save_svg()
# and the masks
mySampCol.save_masks_svg()
mySampCol.save_masks_dxf(labels=False)
mySampCol.save_dxf()