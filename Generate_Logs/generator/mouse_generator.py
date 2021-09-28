import random
import logging

'''
Generate a random mouse position within an area.
The arguments are:
    - Down left position of the visual element (button, checkbox, table, etc.) 
    - Screenshot resolution, for position limits
    - Height and width values for calculating the 4 corners of the area
    - chacer log con el aviso del limite de elemento supera resolución
'''
def generate_mouse_position(position, resolution,height ,width):
    position_h = position[0]
    position_w = position[1]
    if position_h+height > resolution[0]:
        height = resolution[0]-position_h
        logging.warn("Limit of heigh change for resolution limits to: "+str(height))
    if position_w+width > resolution[1]:
        width = resolution[1]-position_w
        logging.warn("Limit of width change for resolution limits to: "+str(width))
    new_height = random.randint(0, height)
    new_width = random.randint(0, width)
    position_h = position_h+new_height
    position_W = position_w+new_width
    return (position_h,position_W)

