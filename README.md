# Python svg samples collection designer

This Python script allows you to create a modified `.svg` rappresenting a flat samples collection. A flat samples collection is a group of flat samples (e.g. some pieces of metals with different varnishes, a series of coloured tile ...). The samples are contained in a samples holder that can be used as reference system.

### Create, automate measurments and visualize
The `.svg`use the standard color coding of laser cutters so you can cut the samples and the samples holder with your laser cutter. If you don't have one you can find a [FabLab next to you](https://www.google.com/maps/search/fablab/) or use an [online service](https://www.google.com/search?q=online+laser+cutting).

Once you have your physical samples collection,if you have a positioning system (microscope stages, linear stages etc. etc) you can use the coordinates inside the `.svg` file for positioning your instrument on the sample (or the part of the sample) you are interested in.

The `.svg`can be read with any browser. The mouse over tooltip can show to anybody what's the last layer of your sample.


### Create an .svg samples collection


```python
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
```
The result is the following:

![Alt text](examples/Test samples collection.svgg)
<img src="examples/Test samples collection.svg">

### Read and query the .svg file

### Installation
You can install it using pip from terminal or from the ipython console:

    pip install git+https://github.com/giacomomarchioro/pysvgsamplescollection


### Requirments

For plotting and querying the collection shapely is required.




