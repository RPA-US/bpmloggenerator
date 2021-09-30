import random
import logging

'''
Generate a random mouse position within an area.
The arguments are:
    - Down left position of the visual element (button, checkbox, table, etc.) 
    - Screenshot resolution, for position limits
    - Height and width values for calculating the 4 corners of the area
'''
def generate_mouse_position(list):
    position_h = list[0]
    position_w = list[1]
    resolution_h = list[2]
    resolution_w = list[3]
    height = list[4]
    width = list[5]
    if position_h+height > resolution_h:
        height = resolution_h-position_h
        logging.warn("Limit of heigh change for resolution limits to: "+str(height))
    if position_w+width > resolution_w:
        width = resolution_w-position_w
        logging.warn("Limit of width change for resolution limits to: "+str(width))
    new_height = random.randint(0, height)
    new_width = random.randint(0, width)
    position_h = position_h+new_height
    position_W = position_w+new_width
    return (position_h,position_W)
