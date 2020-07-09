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
mySampCol.save_svg()
mySampCol.save_masks_svg()
