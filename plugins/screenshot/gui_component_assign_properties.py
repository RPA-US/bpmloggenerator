from PIL import Image
import json

def gui_component_status(args):
    """
    This function takes as argument an UI element status and set it as its property in the json properties
    """
    status = args[0][0]
    image_path_to_save = str(args[1])
    capture = str(args[2])
    process_info = args[len(args)-1]
    process_info["object_json_properties"]["status"] = status
    
    # Simply replicate the screenshot
    capture_img = Image.open(capture)
    original_img = capture_img.copy()
    original_img.save(str(image_path_to_save), quality=95, format="png")

    return status, process_info["object_json_properties"]
    