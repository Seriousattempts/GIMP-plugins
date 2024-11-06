#!/usr/bin/env python

from gimpfu import *

def html_to_rgb(html_color):
    html_color = html_color.lstrip('#')
    return tuple(int(html_color[i:i+2], 16) for i in (0, 2, 4))

def replace_colors_in_layer(image, layer, new_color):
    pdb.gimp_image_undo_group_start(image)
    
    # Create a new layer filled with the new color
    new_layer = gimp.Layer(image, "Color Replacement", layer.width, layer.height, RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_image_insert_layer(image, new_layer, None, 0)
    pdb.gimp_context_set_foreground(new_color)
    pdb.gimp_drawable_fill(new_layer, FOREGROUND_FILL)
    
    # Copy the alpha channel from the original layer
    pdb.gimp_edit_copy(layer)
    float_sel = pdb.gimp_edit_paste(new_layer, True)
    pdb.gimp_floating_sel_anchor(float_sel)
    
    # Set the layer mode to NORMAL and copy it back to the original layer
    pdb.gimp_layer_set_mode(new_layer, NORMAL_MODE)
    pdb.gimp_edit_copy(new_layer)
    float_sel = pdb.gimp_edit_paste(layer, True)
    pdb.gimp_floating_sel_anchor(float_sel)
    
    # Remove the temporary layer
    pdb.gimp_image_remove_layer(image, new_layer)
    
    pdb.gimp_image_undo_group_end(image)

def find_layers_in_group(group, search_term):
    layers_to_process = []
    for layer in group.layers:
        if pdb.gimp_item_is_group(layer):
            if search_term.lower() in pdb.gimp_item_get_name(layer).lower():
                layers_to_process.extend(find_layers_in_group(layer, ""))
            else:
                layers_to_process.extend(find_layers_in_group(layer, search_term))
        elif not search_term or search_term.lower() in pdb.gimp_item_get_name(layer).lower():
            layers_to_process.append(layer)
    return layers_to_process

def replace_colors_in_groups(image, drawable, search_term, html_color):
    new_color = html_to_rgb(html_color)
    
    pdb.gimp_image_undo_group_start(image)
    
    layers_to_process = find_layers_in_group(image, search_term)
    
    for layer in layers_to_process:
        replace_colors_in_layer(image, layer, new_color)
    
    pdb.gimp_image_undo_group_end(image)
    gimp.displays_flush()

register(
    "python_fu_replace_alpha_in_groups_with_colors",
    "Replace alpha channel in layers within groups containing a search term",
    "Replaces every alpha channel in layers within groups containing a search term with a specified HTML color",
    "Jordan B",
    "J",
    "2024",
    "<Image>/Colors/Replace Alpha Channel of a Group of Layers...",
    "*",
    [
        (PF_STRING, "search_term", "Group Name Search Term", ""),
        (PF_STRING, "html_color", "Replacement HTML Color", "#FFFFFF")
    ],
    [],
    replace_colors_in_groups
)

main()
