from PIL import Image
import PIL
from PIL import Image, ImageFont, ImageDraw
# ImageFile.LOAD_TRUNCATED_IMAGES = True
import bpmloggenerator.generic_utils as util
from bpmloggenerator.settings import sep


###################################################################################################
# AUXILIAR FUNCTIONS ##############################################################################
###################################################################################################

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


def replace_gui_element_and_save(image_path_to_save, image_gui_element, newsize, capture, coordinates, left_top_x, left_top_y, back_im):
    if ".png" in str(image_path_to_save):
        rectangle_color = "#ffffff"
        coordinates = [int(coordinates[0]),int(coordinates[1]),int(coordinates[2]),int(coordinates[3])]

        image_gui_element = image_gui_element.convert("RGBA")
        upper_im = image_gui_element.copy()
        # Resize gui element
        upper_im = upper_im.resize(newsize, PIL.Image.NEAREST)
        # Open capture
        capture_img = Image.open(str(capture)).convert("RGBA")
        if not back_im:
            back_im = capture_img.copy()
        
        draw = ImageDraw.Draw(back_im)  
        draw.rectangle(coordinates, fill =rectangle_color, outline =rectangle_color)
        
        back_im.paste(upper_im,(int(left_top_x),int(left_top_y)), upper_im)
        back_im.save(str(image_path_to_save), quality=95, format="png")
        h = upper_im.height
        w = upper_im.width
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
        h, w, c = upper_im.shape
    ui_element_coords = [[int(left_top_x), int(left_top_x)+w], [int(left_top_y), int(left_top_y)+h], w, h]
    return ui_element_coords

###################################################################################################

###################################################################################################
# Generic UI Elements
###################################################################################################
def replace_gui_element_by_other(args):
    '''
    An input capture is obtained, and a visual element is inserted into it​
    args:​
        capture: path of the image to insert in
        coordinates: list with the 2 corners limits of the visual element (left_top_x,left_top_y,right_bot_x,right_bot_y). The coordenate (0,0) is the top_left in the image
        id_element: id of the visual element to be inserted
        image_path_to_save: path where to save the image
    '''
    if "dependency_res" in args:
        selected_element = str(args["dependency_res"])
    else:
        if isinstance(args["gui_elements_to_replace"], list):
            selected_element = util.select_random_list(args["gui_elements_to_replace"])
        else:
            selected_element = str(args[0])
    
    image_element = util.detect_element(selected_element)       
        
    image_path_to_save = args["image_path_to_save"]
    capture = args["original_image_path"]
    coordinates = args["coordinates"]


    # Coordenates x and y
    left_top_x = int(coordinates[0])
    left_top_y = int(coordinates[1])
    right_bot_x = int(coordinates[2])
    right_bot_y = int(coordinates[3])
        
    # Open gui element
    image_gui_element = Image.open(image_element)
            
    # New size element id
    width_size = right_bot_x-left_top_x
    height_size = right_bot_y-left_top_y
    
    if len(coordinates)>4: # [571, 167, 627, 240, "RATIO"] to respect aspect ratio
        newsize = resize_respecting_ratio(width_size, height_size, image_gui_element)
        coordinates = coordinates[:4]
    else:
        newsize = (width_size,height_size)

    ui_element_coords = replace_gui_element_and_save(image_path_to_save, image_gui_element, newsize, capture, coordinates, left_top_x, left_top_y, None)
    
    return {"res": selected_element, "bounding_box": ui_element_coords}


def replace_gui_element_various_places(args):
    '''
    An input capture is obtained, and a "n" visual element is inserted into it​
    args:​
        capture: path of the image to insert in
        coordinates: list with the list of corners limits of the visuals elements: [...for each replacement (left_top_x,left_top_y,right_bot_x,right_bot_y)]. The coordenate (0,0) is the top_left in the image
        id_element: id of the visual element to be inserted
        image_path_to_save: path where to save the image
    '''
    if "dependency_res" in args:
        selected_element = str(args["dependency_res"])
    else:
        if isinstance(args["gui_elements_to_replace"], list):
            selected_element = util.select_random_list(args["gui_elements_to_replace"])
        else:
            selected_element = str(args[0])
    
    image_path_to_save = args["image_path_to_save"]
    capture = args["original_image_path"]
    coordinates = args["coordinates"]

    image_element = str(util.detect_element(selected_element))

    # Open capture: can be abstracted not using replace_gui_element_and_save
    capture_img = Image.open(capture)
    back_im = capture_img.copy()

    # Open gui element
    image_gui_element = Image.open(image_element)
    bounding_boxes = []
    
    for i in range(0, len(coordinates)):
        # Coordenates x and y
        left_top_x = int(coordinates[i][0])
        left_top_y = int(coordinates[i][1])
        right_bot_x = int(coordinates[i][2])
        right_bot_y = int(coordinates[i][3])
        # New size element id
        width_size = right_bot_x-left_top_x
        height_size = right_bot_y-left_top_y

        if len(coordinates[i])>4: # [571, 167, 627, 240, "RATIO"] to respect aspect ratio
            newsize = resize_respecting_ratio(width_size, height_size, image_gui_element)
            coordinates[i] = coordinates[i][:4]
        else:
            newsize = (width_size,height_size)
        
        bounding_boxes.append(replace_gui_element_and_save(image_path_to_save, image_gui_element, newsize, capture, coordinates[i], left_top_x, left_top_y, back_im))
       
    return {"res": selected_element, "bounding_box": bounding_boxes}

def hidden_gui_element(args):
    '''
    An input capture is obtained, and a gui element is hidden​
    args:​
        capture: path of the image to insert in
        coordinates: list with the 2 corners limits of the visual element (left_top_x,left_top_y,right_bot_x,right_bot_y). The coordenate (0,0) is the top_left in the image
        new_image: saved image
        configuration: background color (p.e. #FFFFF)
    '''
    # configuration = str(util.select_random_list(args[0]))
    new_image = args["image_path_to_save"]
    capture = args["original_image_path"]
    coordinates = args["coordinates"]
    coordinates = [int(coordinates[0]),int(coordinates[1]),int(coordinates[2]),int(coordinates[3])]

    # Configuration
    rectangle_color = args["color_hidden_square"]
    # Open capture
    capture_img = Image.open(capture)
    back_im = capture_img.copy()
    # Hidden element
    draw = ImageDraw.Draw(back_im)  
    draw.rectangle(coordinates, fill =rectangle_color, outline =rectangle_color)
    # Save image
    back_im.save(new_image, quality=95)
    if sep in new_image:
        splitted = new_image.split(sep)
        new_image = splitted[len(splitted)-1]
    return {"res": new_image, "bounding_box": [[int(coordinates[0]),int(coordinates[1])],[int(coordinates[2]),int(coordinates[3])], int(coordinates[2]) - int(coordinates[0]), int(coordinates[3]) - int(coordinates[1])]}



###################################################################################################
# Text UI Elements (Output for all functions in text_in_image)
###################################################################################################
def insert_text_image(args):
    '''
    An input capture is obtained, and a text is inserted into it​
    args:​
        text: the text to be inserted
        font_configuration: path to the font type; integer of the font size; color of the font; background color
        new_image: path to saved image
        capture: path of the image to insert in
        coordinates: list with the top left corner. The coordenate (0,0) is the top_left in the image
    '''
    
    if "dependency_res" in args:
        text = str(args["dependency_res"])
    else:
        text = args["text_to_insert"]
        
    
    font = str(args["font_configuration"][0])
    font_size = int(args["font_configuration"][1])
    font_color = str(args["font_configuration"][2])
    new_image = args["image_path_to_save"]
    capture = args["original_image_path"]
    if isinstance(args["coordinates"], list):
        coordinates = args["coordinates"]
    background_color = False
    if len(args["font_configuration"]) > 3 and (isinstance(args["font_configuration"], list)):
        background_color = str(args["font_configuration"][3])
    
    # Coordenates x and y
    left_top_x = int(coordinates[0])
    left_top_y = int(coordinates[1])
    coordinates = [int(coordinates[0]),int(coordinates[1]),int(coordinates[2]),int(coordinates[3])]

    if background_color:
        capture_img = Image.open(capture)
        back_im = capture_img.copy()
        draw = ImageDraw.Draw(back_im)  
        draw.rectangle(coordinates, fill=background_color, outline=background_color)
        # Save image
        back_im.save(new_image, quality=95)
    else:
        # Open capture
        capture_img = Image.open(capture)
        back_im = capture_img.copy()
        # Create text
        draw = ImageDraw.Draw(back_im)
    
    font = ImageFont.truetype(font, int(font_size))
    
    # Obtener el tamaño del texto
    text_width, text_height = draw.textsize(text, font=font)
    
    resulting_text_coordinates = [[left_top_x, left_top_x+text_width], [left_top_y, left_top_y+text_width], text_width, text_height]
    
    # Dibuja el texto en la imagen
    draw.text((left_top_x, left_top_y), text, font_color, font=font)
    
    # Save image
    back_im.save(new_image, quality=95)
    if sep in new_image:
        splitted = new_image.split(sep)
        new_image = splitted[len(splitted)-1]
    
    return {"res": text, "bounding_box": resulting_text_coordinates}