import random
import logging


def generate_mouse_position(args):
    '''
    Generate a random mouse position within an area.
    args:
        args: List with required position
            - Down left position of the visual element (button, checkbox, table, etc.) 
            - Screenshot resolution, for position limits
            - Height and width values for calculating the 4 corners of the area
    '''
    position_h = args[0]
    position_w = args[1]
    resolution_h = liargsst[2]
    resolution_w = args[3]
    height = args[4]
    width = args[5]
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

def generate_mouse_position_x(args):
    '''
    Generate a random mouse position for x cordenate within an area.
    args:
        args: List with required position
            - Down left position of the visual element (button, checkbox, table, etc.) 
            - Screenshot resolution, for x position limits
            - Width values for calculating the corner of the area
    '''
    position_w = args[0]
    resolution_w = args[1]
    width = args[2]
    if position_w+width > resolution_w:
        width = resolution_w-position_w
        logging.warn("Limit of width change for resolution limits to: "+str(width))
    new_width = random.randint(0, width)
    position_W = position_w+new_width
    return position_W

   

def generate_mouse_position_y(args):
    '''
    Generate a random mouse position for y cordenate within an area.
    The arguments are:
        args:
        args: List with required position
            - Down left position of the visual element (button, checkbox, table, etc.) 
            - Screenshot resolution, for y position limit
            - Height value for calculating the corner of the area
    '''
    position_h = args[0]
    resolution_h = args[1]
    height = args[2]
    if position_h+height > resolution_h:
        height = resolution_h-position_h
        logging.warn("Limit of heigh change for resolution limits to: "+str(height))
    new_height = random.randint(0, height)
    position_h = position_h+new_height
    return position_h
