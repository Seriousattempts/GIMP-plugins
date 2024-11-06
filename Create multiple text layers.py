#!/usr/bin/env python

from gimpfu import *
import re

def increment_number_in_text(text, increment_by):
    def repl(match):
        return str(int(match.group(0)) + increment_by)
    return re.sub(r'\d+', repl, text)

def create_multiple_text_layers(image, drawable, num_layers, text_content, font_name, font_size, text_color,
                                text_pos_x, text_pos_y, text_width, text_height,
                                text_increment, text_increment_by):
    pdb.gimp_image_undo_group_start(image)
    
    for i in range(num_layers):
        if text_increment:
            text_content_with_increment = increment_number_in_text(text_content, i * text_increment_by)
        else:
            text_content_with_increment = text_content
        
        # Create text layer
        text_layer = pdb.gimp_text_layer_new(image, text_content_with_increment, font_name, font_size, 0)
        pdb.gimp_image_insert_layer(image, text_layer, None, -1)
        
        # Resize text layer to fit within the specified area
        pdb.gimp_text_layer_set_justification(text_layer, 2)  # CENTER
        pdb.gimp_text_layer_resize(text_layer, text_width, text_height)
        
        # Position text layer
        pdb.gimp_layer_set_offsets(text_layer, text_pos_x, text_pos_y)
        
        # Set text color
        pdb.gimp_text_layer_set_color(text_layer, text_color)
    
    pdb.gimp_image_undo_group_end(image)
    gimp.displays_flush()

register(
    "python_fu_create_multiple_text_layers",
    "Create multiple text layers",
    "Creates multiple text layers with optional increments",
    "Jordan B",
    "J",
    "2024",
    "<Image>/Layer/Create Multiple Text Layers...",
    "*",
    [
        (PF_INT, "num_layers", "Number of text layers", 1),
        (PF_STRING, "text_content", "Text Content", "Text"),
        (PF_FONT, "font_name", "Font", "Sans"),
        (PF_INT, "font_size", "Font Size", 24),
        (PF_COLOR, "text_color", "Text Color", (0, 0, 0)),
        (PF_INT, "text_pos_x", "Position Text X (top-left)", 0),
        (PF_INT, "text_pos_y", "Position Text Y (top-left)", 0),
        (PF_INT, "text_width", "Size Text (Width)", 100),
        (PF_INT, "text_height", "Size Text (Height)", 24),
        (PF_TOGGLE, "text_increment", "Increment Text Number", FALSE),
        (PF_INT, "text_increment_by", "Text Increment By", 1),
    ],
    [],
    create_multiple_text_layers
)

main()
