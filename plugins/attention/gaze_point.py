import random
import logging


def gaze_point_in_range(args):
    '''
    Generate a random gaze point within an area corresponding to a UI element.
    args:
        args: List with required position
            - Down left position of the visual element (button, checkbox, table, etc.) 
            - Screenshot resolution, for position limits
            - Height and width values for calculating the 4 corners of the area
    '''
    position_h = int(args[0])
    position_w = int(args[1])
    resolution_h = int(liargsst[2])
    resolution_w = int(args[3])
    height = int(args[4])
    width = int(args[5])
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