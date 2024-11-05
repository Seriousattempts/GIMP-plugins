#!/usr/bin/env python

from gimpfu import *

def replace_layer_with_image(image, layer, replacement_image_path):
    # Load the replacement image as a new layer
    replacement_layer = pdb.gimp_file_load_layer(image, replacement_image_path)
    
    # Get the current layer's attributes
    name = pdb.gimp_item_get_name(layer)
    visible = pdb.gimp_item_get_visible(layer)
    opacity = pdb.gimp_layer_get_opacity(layer)
    mode = pdb.gimp_layer_get_mode(layer)
    width = layer.width
    height = layer.height
    offsets = layer.offsets
    mask = pdb.gimp_layer_get_mask(layer)
    parent = pdb.gimp_item_get_parent(layer)
    
    # Add the replacement layer to the image
    position = pdb.gimp_image_get_item_position(image, layer)
    pdb.gimp_image_insert_layer(image, replacement_layer, parent, position)
    
    # Scale the replacement layer content
    pdb.gimp_layer_scale(replacement_layer, width, height, True)
    
    # Apply the original layer's attributes to the replacement layer
    pdb.gimp_item_set_name(replacement_layer, name)
    pdb.gimp_item_set_visible(replacement_layer, visible)
    pdb.gimp_layer_set_opacity(replacement_layer, opacity)
    pdb.gimp_layer_set_mode(replacement_layer, mode)
    pdb.gimp_layer_set_offsets(replacement_layer, offsets[0], offsets[1])
    
    # Copy the layer mask if it exists
    if mask:
        new_mask = pdb.gimp_layer_create_mask(replacement_layer, ADD_MASK_WHITE)
        pdb.gimp_layer_add_mask(replacement_layer, new_mask)
        pdb.gimp_edit_copy(mask)
        floating_sel = pdb.gimp_edit_paste(new_mask, True)
        pdb.gimp_floating_sel_anchor(floating_sel)
    
    # Remove the original layer
    pdb.gimp_image_remove_layer(image, layer)

def find_layers_by_name(image, group, search_term):
    matching_layers = []
    for layer in group.layers:
        if pdb.gimp_item_is_group(layer):
            matching_layers.extend(find_layers_by_name(image, layer, search_term))
        elif search_term.lower() in layer.name.lower():
            matching_layers.append(layer)
    return matching_layers

def replace_layers_with_image(image, drawable, search_term, replacement_image_path):
    matching_layers = find_layers_by_name(image, image, search_term)
    
    for layer in matching_layers:
        replace_layer_with_image(image, layer, replacement_image_path)
    
    gimp.displays_flush()

register(
    "python_fu_replace_layers_with_image",
    "Replace layers containing a search term with an image",
    "Replaces layers containing a search term with a specified image file, preserving layer attributes",
    "Your Name",
    "Your Name",
    "2024",
    "<Image>/Layer/Replace Specific Layers with Image...",
    "*",
    [
        (PF_STRING, "search_term", "Search Term", ""),
        (PF_FILE, "replacement_image_path", "Replacement Image", "")
    ],
    [],
    replace_layers_with_image
)

main()
