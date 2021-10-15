import random
import time
from PIL import Image
import os
import PIL
import glob


def replace_gui_element_by_other(capture, coordenates, image_element,new_image):
    '''
    An input capture is obtained, and a visual element is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the 2 corners limits of the visual element. The coordenate (0,0) is the top_left in the image
        id_element: id of the visual element to be inserted
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
