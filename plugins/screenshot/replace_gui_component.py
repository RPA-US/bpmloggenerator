from PIL import Image
import PIL
import shutil
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from lorem_text import lorem
import agosuirpa.generic_utils as util
import sqlite3 as sl
from agosuirpa.system_configuration import sep
import random

def resize_respecting_ratio(width_size, height_size, image):
    image_width = image.size[0]
    image_height = image.size[1]
    width_size = int(width_size)
    height_size = int(height_size)
    if width_size - image_width < height_size - image_height:
        height_percent = (height_size / float(image.size[1]))
        width_size = int((float(image.size[0]) * float(height_percent)))
    else:
        width_percent = (width_size / float(image.size[0]))
        height_size = int((float(image.size[1]) * float(width_percent)))
    return (width_size, height_size)


def replace_gui_element_by_other(args):
    '''
    An input capture is obtained, and a visual element is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the 2 corners limits of the visual element (left_top_x,left_top_y,right_bot_x,right_bot_y). The coordenate (0,0) is the top_left in the image
        id_element: id of the visual element to be inserted
        image_path_to_save: path where to save the image
    '''
    if len(args) > 4:
        selected_element = str(args[4])
        image_element = util.detect_element(selected_element)       
    elif isinstance(args[0], list):
        selected_element = util.select_random_list(args[0])
        image_element = util.detect_element(selected_element)
    else:
        selected_element = str(args[0])
        image_element = util.detect_element(selected_element)
    image_path_to_save = str(args[1])
    capture = str(args[2])
    coordenates = args[3]


    # Coordenates x and y
    left_top_x = int(coordenates[0])
    left_top_y = int(coordenates[1])
    right_bot_x = int(coordenates[2])
    right_bot_y = int(coordenates[3])
        
    # Open gui element
    image_gui_element = Image.open(image_element)
            
    # New size element id
    width_size = right_bot_x-left_top_x
    height_size = right_bot_y-left_top_y
    
    if len(coordenates)>4: # [571, 167, 627, 240, "RATIO"] to respect aspect ratio
        newsize = resize_respecting_ratio(width_size, height_size, image_gui_element)
        coordenates = coordenates[:4]
    else:
        newsize = (width_size,height_size)
    
        
    replace_gui_element_and_save(image_path_to_save, image_gui_element, newsize, capture, coordenates, left_top_x, left_top_y, None)
    
    return selected_element

def replace_gui_element_and_save(image_path_to_save, image_gui_element, newsize, capture, coordenates, left_top_x, left_top_y, back_im):
    if ".png" in str(image_path_to_save):
        rectangle_color = "#ffffff"
        coordenates = [int(coordenates[0]),int(coordenates[1]),int(coordenates[2]),int(coordenates[3])]

        image_gui_element = image_gui_element.convert("RGBA")
        upper_im = image_gui_element.copy()
        # Resize gui element
        upper_im = upper_im.resize(newsize, PIL.Image.NEAREST)
        # Open capture
        capture_img = Image.open(str(capture)).convert("RGBA")
        if not back_im:
            back_im = capture_img.copy()
        
        draw = ImageDraw.Draw(back_im)  
        draw.rectangle(coordenates, fill =rectangle_color, outline =rectangle_color)
        
        back_im.paste(upper_im,(int(left_top_x),int(left_top_y)), upper_im)
        back_im.save(str(image_path_to_save), quality=95, format="png")
    else:
        upper_im = image_gui_element.copy()
        # Resize gui element
        upper_im = upper_im.resize(int(newsize), PIL.Image.NEAREST)
        # Open capture
        capture_img = Image.open(str(capture))
        if not back_im:
            back_im = capture_img.copy()
        back_im.paste(upper_im,(int(left_top_x),int(left_top_y)), upper_im)
        back_im.save(str(image_path_to_save), quality=95)

def replace_gui_element_various_places(args):
    '''
    An input capture is obtained, and a "n" visual element is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the list of corners limits of the visuals elements: [...for each replacement (left_top_x,left_top_y,right_bot_x,right_bot_y)]. The coordenate (0,0) is the top_left in the image
        id_element: id of the visual element to be inserted
        image_path_to_save: path where to save the image
    '''
    if len(args) > 4:
        selected_element = str(args[4])
    elif isinstance(args[0], list):
        selected_element = str(util.select_random_list(args[0]))
    image_path_to_save = str(args[1])
    capture = str(args[2])
    if isinstance(args[3], list):
        coordenates = args[3]

    image_element = str(util.detect_element(selected_element))

    # Open capture: can be abstracted not using replace_gui_element_and_save
    capture_img = Image.open(capture)
    back_im = capture_img.copy()

    # Open gui element
    image_gui_element = Image.open(image_element)

    for i in range(0, len(coordenates)):
        # Coordenates x and y
        left_top_x = int(coordenates[i][0])
        left_top_y = int(coordenates[i][1])
        right_bot_x = int(coordenates[i][2])
        right_bot_y = int(coordenates[i][3])
        # New size element id
        width_size = right_bot_x-left_top_x
        height_size = right_bot_y-left_top_y

        if len(coordenates[i])>4: # [571, 167, 627, 240, "RATIO"] to respect aspect ratio
            newsize = resize_respecting_ratio(width_size, height_size, image_gui_element)
            coordenates[i] = coordenates[i][:4]
        else:
            newsize = (width_size,height_size)
        
        replace_gui_element_and_save(image_path_to_save, image_gui_element, newsize, capture, coordenates[i], left_top_x, left_top_y, back_im)
       
    return selected_element

def hidden_gui_element(args):
    '''
    An input capture is obtained, and a gui element is hidden​
    args:​
        capture: path of the image to insert in
        coordenates: list with the 2 corners limits of the visual element (left_top_x,left_top_y,right_bot_x,right_bot_y). The coordenate (0,0) is the top_left in the image
        new_image: saved image
        configuration: background color (p.e. #FFFFF)
    '''
    configuration = str(util.select_random_list(args[0]))
    new_image = str(args[1])
    capture = str(args[2])
    coordenates = args[3]
    coordenates = [int(coordenates[0]),int(coordenates[1]),int(coordenates[2]),int(coordenates[3])]

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
    if sep in new_image:
        splitted = new_image.split(sep)
        new_image = splitted[len(splitted)-1]
    return new_image


def generate_copied_capture(args):
    '''
    Generate an image copy renamed
    '''
    capture = str(args[0])
    generate_path = str(args[1])
    number = args[2]
    if not '.png' in str(number):
        name = generate_path+str(number)+"_img.png"
    else:
        name = generate_path+str(number)
    shutil.copyfile(capture, name)
    # Random number and the extension with a img identification
    return name

def generate_copied_capture_without_root(args):
    '''
    Generate an image copy renamed
    '''
    capture = str(args[0])
    generate_path = str(args[1])
    number = args[2]
    name = str(number)+"_img.png"
    shutil.copyfile(capture, generate_path+name)
    # Random number and the extension with a img identification
    return name

########################
# INSERT TEXT IN IMAGE #
########################

def delimit_characters(s, char_limit):
    res = "".join(s[i:i+char_limit] + "\n" for i in range(0,len(s),char_limit))
    return res

def random_word_image(args):
    """
    Mandatory to have as args Font, Font size, Font color, Background color, Character delimitation, Random max number of word: "args": ["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF", 84, 3]
    """
    if args[0] and len(list(args[0]))>5:
        size = random.randint(1,int(args[0][5]))
    else:
        size = 1
    s = lorem.words(size)
    s_line_breaks = delimit_characters(s,int(args[0][4]))
    return random_text_image(args,s_line_breaks)
    
def random_paragraph_image(args):
    """
    Mandatory to have as args Font, Font size, Font color, Background color, Character delimitation, Random max number of paragraph: "args": ["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF", 84, 3]
    """
    if args[0] and len(list(args[0]))>5:
        size = random.randint(1,int(args[0][5]))
    else:
        size = random.randint(1,2)
    s = lorem.paragraphs(size)
    s_line_breaks = delimit_characters(s,int(args[0][4]))
    return random_text_image(args,s_line_breaks)
    
def random_sentence_image(args):
    """
    Mandatory to have as args Font, Font size, Font color, Background color and Character delimitation for paragraph: "args[0]":["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF", 84]
    """
    s = lorem.sentence()
    s_line_breaks = delimit_characters(s,int(args[0][4]))
    return random_text_image(args,s_line_breaks)

def random_text_image(args,random_text):
    '''
    An input capture is obtained, and a text is inserted into it​
    args:​
        capture: path of the image to insert in
        coordenates: list with the top left corner. The coordenate (0,0) is the top_left in the image
        text: the text to be inserted
        new_image: saved image
        configuration: path to the font type; integer of the font size; the tuple of the font color
    '''
    
    args_aux = args
    
    # hide background
    args_aux.insert(0,str(random_text))
    return insert_text_image(args_aux)


def insert_text_image(args):
    '''
    An input capture is obtained, and a text is inserted into it​
    args:​
        text: the text to be inserted
        font_configuration: path to the font type; integer of the font size; the tuple of the font color
        new_image: path to saved image
        capture: path of the image to insert in
        coordenates: list with the top left corner. The coordenate (0,0) is the top_left in the image
    '''
    text = str(args[0])
    font = str(args[1][0])
    font_size = int(args[1][1])
    font_color = str(args[1][2])
    new_image = str(args[2])
    capture = str(args[3])
    if isinstance(args[4], list):
        coordenates = args[4]
    background_color = False
    if len(args[1]) > 3:
        background_color = str(args[1][3])
    
    # Coordenates x and y
    left_top_x = int(coordenates[0])
    left_top_y = int(coordenates[1])
    coordenates = [int(coordenates[0]),int(coordenates[1]),int(coordenates[2]),int(coordenates[3])]

    if len(args) > 5:
        text =  str(args[5])
        capture_img = Image.open(capture)
        back_im = capture_img.copy()
        draw = ImageDraw.Draw(back_im)  
        draw.rectangle(coordenates, fill ="#ffffff", outline ="#ffffff")
        # Save image
        back_im.save(new_image, quality=95)
    elif background_color:
        capture_img = Image.open(capture)
        back_im = capture_img.copy()
        draw = ImageDraw.Draw(back_im)  
        draw.rectangle(coordenates, fill =background_color, outline =background_color)
        # Save image
        back_im.save(new_image, quality=95)
    else:
        # Open capture
        capture_img = Image.open(capture)
        back_im = capture_img.copy()
        # Create text
        draw = ImageDraw.Draw(back_im)
    
    font = ImageFont.truetype(font, int(font_size))
    draw.text((left_top_x, left_top_y),text,font_color,font=font)
    # Save image
    back_im.save(new_image, quality=95)
    if sep in new_image:
        splitted = new_image.split(sep)
        new_image = splitted[len(splitted)-1]
    return text