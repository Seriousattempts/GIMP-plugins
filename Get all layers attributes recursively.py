#!/usr/bin/env python

from gimpfu import *

def get_layer_attributes(layer, indent=""):
    pdb.gimp_message(indent + "Layer: " + layer.name)
    pdb.gimp_message(indent + "Visible: " + str(layer.visible))
    pdb.gimp_message(indent + "Opacity: " + str(layer.opacity))
    pdb.gimp_message(indent + "Mode: " + str(layer.mode))
    pdb.gimp_message(indent + "Width: " + str(layer.width))
    pdb.gimp_message(indent + "Height: " + str(layer.height))
    pdb.gimp_message(indent + "Offsets: " + str(layer.offsets))
    pdb.gimp_message(indent + "Mask: " + str(layer.mask))
    pdb.gimp_message(indent + "------------------------")

    if isinstance(layer, gimp.GroupLayer):
        for child_layer in layer.layers:
            get_layer_attributes(child_layer, indent + "  ")

def process_image(image, drawable):
    for layer in image.layers:
        get_layer_attributes(layer)

register(
    "python_fu_get_all_layer_attributes",
    "Get attributes of all layers including those in groups",
    "Prints attributes of all layers in the image, including those within layer groups",
    "Your Name",
    "Your Name",
    "2024",
    "<Image>/Filters/Get All Layer Attributes",
    "*",
    [],
    [],
    process_image
)

main()
