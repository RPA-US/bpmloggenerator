from PIL import Image
import json
from .replace_gui_component import replace_gui_element_and_save, resize_respecting_ratio
import bpmloggenerator.generic_utils as util
from bpmloggenerator.settings import sep
from lorem_text import lorem
from PIL import Image, ImageDraw, ImageFont

# color = (255, 244, 41)
# text = 'S'

# N = 500
# size_image = width_image, height_image = N, N

# img = Image.new('RGB', size_image, color='white')
# font_path = './fonts/BebasNeue-Regular.ttf'
# font = ImageFont.truetype(font_path, size=600)
# draw = ImageDraw.Draw(img)
# width_text, height_text = draw.textsize(text, font)

# offset_x, offset_y = font.getoffset(text)
# width_text += offset_x
# height_text += offset_y

# top_left_x = width_image / 2 - width_text / 2
# top_left_y = height_image / 2 - height_text / 2
# xy = top_left_x, top_left_y

# draw.text(xy, text, font=font, fill=color)

# img.show()

###############################################################################
# Auxiliar
###############################################################################
def modify_gui_component_status(status, object_json_properties):
    if ";" in status:
        status_list = status.split(";")
        for index, s in enumerate(status_list):
            if "," in s:
                keyvalue = s.split(",")
                object_json_properties["st_"+keyvalue[0]] = keyvalue[1]
            else:
                object_json_properties["st_"+str(index)] = s
    else:
        if "," in status:
                keyvalue = status.split(",")
                object_json_properties["st_"+keyvalue[0]] = keyvalue[1]
        else:
            object_json_properties["st_0"] = status
    return object_json_properties
###############################################################################

def gui_component_status(args):
    """
    This function takes as argument an UI element status and set it as its property in the json properties
    """
    status = args["gui_component_status"]
    process_info = args["process_info"]
    process_info["object_json_properties"] = modify_gui_component_status(status, process_info["object_json_properties"])
    
    image_path_to_save = args["image_path_to_save"]
    capture = args["original_image_path"]
    
    # Simply replicate the screenshot
    capture_img = Image.open(capture)
    original_img = capture_img.copy()
    original_img.save(str(image_path_to_save), quality=95, format="png")

    return {"res": status, "object_properties": process_info["object_json_properties"]}