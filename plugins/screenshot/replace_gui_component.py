import random
import time
from PIL import Image
import os
import PIL
import glob
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def replace_gui_element_by_other(capture, coordenates, image_element,new_image):
    '''
    An input capture is obtained, and a visual element is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the 2 corners limits of the visual element (left_top_x,left_top_y,right_bot_x,right_bot_y). The coordenate (0,0) is the top_left in the image
        id_element: id of the visual element to be inserted
        new_image: saved image
    '''
    # Coordenates x and y
    left_top_x = coordenates[0]
    left_top_y = coordenates[1]
    right_bot_x = coordenates[2]
    right_bot_y = coordenates[3]
    # New size element id
    width_size = right_bot_x-left_top_x
    height_size = right_bot_y-left_top_y
    newsize = (width_size,height_size)
    # Open gui element
    image_element = Image.open(image_element)
    upper_im = image_element.copy()
    # Resize gui element
    upper_im = upper_im.resize(newsize, PIL.Image.NEAREST)
    # Open capture
    capture_img = Image.open(capture)
    back_im = capture_img.copy()
    back_im.paste(upper_im,(left_top_x,left_top_y))
    back_im.save(new_image, quality=95)


def insert_text_image(capture, coordenates, text, new_image, configuration):
    '''
    An input capture is obtained, and a text is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the top left corner. The coordenate (0,0) is the top_left in the image
        text: the text to be inserted
        new_image: saved image
        configuration: path to the font type; integer of the font size; the tuple of the font color
    '''
    # Coordenates x and y
    left_top_x = coordenates[0]
    left_top_y = coordenates[1]
    # Configuration
    font = configuration[0]
    font_size = configuration[1]
    font_color = configuration[2]
    # Open capture
    capture_img = Image.open(capture)
    back_im = capture_img.copy()
    # Create text
    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype(font, font_size)
    draw.text((left_top_x, left_top_y),text,font_color,font=font)
    # Save image
    back_im.save(new_image, quality=95)

def hidden_gui_element(capture, coordenates, new_image, configuration):
    '''
    An input capture is obtained, and a gui element is hidden​
    args:​
        capture: path of the image to insert in
        coordenates: list with the 2 corners limits of the visual element (left_top_x,left_top_y,right_bot_x,right_bot_y). The coordenate (0,0) is the top_left in the image
        new_image: saved image
        configuration: path to the font type; integer of the font size; the tuple of the font color
    '''
    # Configuration
    rectangle_color = configuration[0]
    # Open capture
    capture_img = Image.open(capture)
    back_im = capture_img.copy()
    # Hidden element
    draw = ImageDraw.Draw(back_im)  
    draw.rectangle(coordenates, fill =rectangle_color, outline =rectangle_color)
    # Save image
    back_im.save(new_image, quality=95)


