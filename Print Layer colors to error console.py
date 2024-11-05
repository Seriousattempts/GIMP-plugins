#!/usr/bin/env python

from gimpfu import *

def get_unique_colors(layer):
    pixel_region = layer.get_pixel_rgn(0, 0, layer.width, layer.height, False, False)
    unique_colors = set()

    for y in range(layer.height):
        for x in range(layer.width):
            pixel = pixel_region[x, y]
            r, g, b = ord(pixel[0]), ord(pixel[1]), ord(pixel[2])
            unique_colors.add((r, g, b))

    return unique_colors

def print_layer_colors(layer, indent=""):
    pdb.gimp_message(indent + "Layer: " + layer.name)
    
    if isinstance(layer, gimp.GroupLayer):
        pdb.gimp_message(indent + "Group Layer - No direct colors")
        pdb.gimp_message(indent + "------------------------")
        for child_layer in layer.layers:
            print_layer_colors(child_layer, indent + "  ")
    else:
        unique_colors = get_unique_colors(layer)
        pdb.gimp_message(indent + "Unique colors:")
        for color in unique_colors:
            pdb.gimp_message(indent + "  RGB: {}".format(color))
        pdb.gimp_message(indent + "------------------------")

def process_image(image, drawable):
    for layer in image.layers:
        print_layer_colors(layer)

register(
    "python_fu_print_all_layer_colors",
    "Print unique colors of all layers including those in groups",
    "Prints unique colors of all layers in the image, including those within layer groups",
    "Your Name",
    "Your Name",
    "2024",
    "<Image>/Colors/Print Layer colors as RGB",
    "*",
    [],
    [],
    process_image
)

main()
