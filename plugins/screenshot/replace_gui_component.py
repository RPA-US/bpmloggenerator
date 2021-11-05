from PIL import Image
import PIL
import shutil
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import tools.generic_utils as util


def replace_gui_element_by_other(args):
    '''
    An input capture is obtained, and a visual element is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the 2 corners limits of the visual element (left_top_x,left_top_y,right_bot_x,right_bot_y). The coordenate (0,0) is the top_left in the image
        id_element: id of the visual element to be inserted
        image_path_to_save: path where to save the image
    '''
    if isinstance(args[0], list):
        image_element = util.detect_element(util.select_random_list(args[0]))
    else:
        image_element =  args[0]
    image_path_to_save = args[1]
    capture = args[2]
    coordenates = args[3]
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
    back_im.save(image_path_to_save, quality=95)
    return image_path_to_save

def replace_gui_element_various_places(args):
    '''
    An input capture is obtained, and a "n" visual element is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the list of corners limits of the visuals elements: [...for each replacement (left_top_x,left_top_y,right_bot_x,right_bot_y)]. The coordenate (0,0) is the top_left in the image
        id_element: id of the visual element to be inserted
        image_path_to_save: path where to save the image
    '''
    image_element = util.detect_element(util.select_random_list(args[0]))
    image_path_to_save = args[1]
    capture = args[2]
    coordenates = args[3]

    # Open capture
    capture_img = Image.open(capture)
    back_im = capture_img.copy()

    # Open gui element
    image_element = Image.open(image_element)
    upper_im = image_element.copy()

    for i in range(0, len(coordenates)):
        #replace_gui_element_by_other(image_element, image_path_to_save, capture, coordenates[limit])

        # Coordenates x and y
        left_top_x = coordenates[i][0]
        left_top_y = coordenates[i][1]
        right_bot_x = coordenates[i][2]
        right_bot_y = coordenates[i][3]
        # New size element id
        width_size = right_bot_x-left_top_x
        height_size = right_bot_y-left_top_y
        newsize = (width_size,height_size)

        # Resize gui element
        upper_im = upper_im.resize(newsize, PIL.Image.NEAREST)

        back_im.paste(upper_im,(left_top_x,left_top_y))
        back_im.save(image_path_to_save, quality=95)
        
        back_im.paste(upper_im,(left_top_x,left_top_y))
        back_im.save(image_path_to_save, quality=95)
    


def insert_text_image(args):
    '''
    An input capture is obtained, and a text is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the top left corner. The coordenate (0,0) is the top_left in the image
        text: the text to be inserted
        new_image: saved image
        configuration: path to the font type; integer of the font size; the tuple of the font color
    '''
    text = args[0]
    font = args[1][0]
    font_size = args[1][1]
    font_color = args[1][2]
    new_image = args[2]
    capture = args[3]
    coordenates = args[4]
    # Coordenates x and y
    left_top_x = coordenates[0]
    left_top_y = coordenates[1]
    # Open capture
    capture_img = Image.open(capture)
    back_im = capture_img.copy()
    # Create text
    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype(font, int(font_size))
    draw.text((left_top_x, left_top_y),text,font_color,font=font)
    # Save image
    back_im.save(new_image, quality=95)
    return new_image

def hidden_gui_element(args):
    '''
    An input capture is obtained, and a gui element is hidden​
    args:​
        capture: path of the image to insert in
        coordenates: list with the 2 corners limits of the visual element (left_top_x,left_top_y,right_bot_x,right_bot_y). The coordenate (0,0) is the top_left in the image
        new_image: saved image
        configuration: path to the font type; integer of the font size; the tuple of the font color
    '''
    configuration = util.select_random_list(args[0])
    new_image = args[1]
    capture = args[2]
    coordenates = args[3]
    # Configuration
    rectangle_color = configuration
    # Open capture
    capture_img = Image.open(capture)
    back_im = capture_img.copy()
    # Hidden element
    draw = ImageDraw.Draw(back_im)  
    draw.rectangle(coordenates, fill =rectangle_color, outline =rectangle_color)
    # Save image
    back_im.save(new_image, quality=95)
    return new_image


def generate_copied_capture(args):
    '''
    Generate an image copy renamed
    '''
    capture = args[0]
    generate_path = args[1]
    number = args[2]
    name = generate_path+str(number)+"_img.png"
    shutil.copyfile(capture, name)
    # Random number and the extension with a img identification
    return name