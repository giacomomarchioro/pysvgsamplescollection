from svgsamplescollection import Samplescollection
mycollection = Samplescollection()
# We can set the name of the collection
mycollection.name = 'Test samples collection'
# The dimension (better if we use ISO dimenso for reusability)
mycollection.set_samplesholder_dimension.A4()
# Also the dimension of the samples should be standardized
mycollection.set_sample_dimension.Microscope_slide()
mycollection.set_number_of_samples(15)
# Here we create the sample holder
mycollection.create_sample_holder()
mycollection.populate_with_samples('wood')
# we start form the second sample (python start from index 0)
for sample in mycollection.samples[1:]:
    # we add to each sample excpet the first a layer of vermilion egg tempera
    sample.add_layer("vermilion egg tempera", "brush", width_percent=0.9)
for sample in mycollection.samples[1:5]:
    # from the second to the fifth we add a varnish
    sample.add_layer("varnish", "brush", width_percent=0.7)
for sample in mycollection.samples[::2]:
    # eventually we add a treatment using UV light 
    sample.add_treatment("uv curing", 
                            parameters = {"duration": "5 h",
                                        "wavelength_nm":"290"},
                            height_percent=0.5)
for sample in mycollection.samples:
    # finally we clean all the sample using acetone
    sample.add_treatment("cleaning", "acetone",width_percent=0.5)
mycollection.insert_alignment_MTF_standard()
mycollection.insert_scalebar()
mycollection.insert_standard()
# we save the svg file with all the information
mycollection.save_svg()
# and the masks
mycollection.save_masks_svg()
