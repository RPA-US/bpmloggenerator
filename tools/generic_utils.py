import json
import random
import os
from configuration.settings import sep, function_trace, element_trace
# from plugins.string.random_text_lorem import generate_DNI,generate_paragraph,generate_path,generate_random_entity,generate_sentence,generate_words
# from plugins.list.coordenates_in_range import generate_mouse_position, generate_mouse_position_x,generate_mouse_position_y
# from plugins.list.mouse_tipe import generate_mousekeyboard
# from plugins.screenshot.name_screenshot import generate_screenshot_demo, generate_screenshot_without_root_path
# from plugins.screenshot.replace_gui_component import hidden_gui_element, insert_text_image, replace_gui_element_by_other, generate_copied_capture, replace_gui_element_various_places, generate_copied_capture_without_root, random_paragraph_image, random_word_image, random_sentence_image
# from plugins.app.nameapp import generate_app_demo
# from plugins.string.random_timestamp import generate_timestamp
for category in os.scandir('plugins'):
    for entry in os.scandir('plugins/'+category.name):
        if entry.is_file():
            filename = f'{entry.name}'[:-3]
            import_path = f'from plugins.{category.name}.{filename} import *'
            exec (import_path)


def detect_function(text):
    '''
    Selecting a function in the system by means of a keyword
    args:
        text: function to be detected
    '''
    # Search the function by key in the json
    f = open('configuration'+sep+function_trace)
    json_func = json.load(f)
    return eval(json_func[text])

def detect_element(text):
    '''
    Selecting an element in the system by means of a keyword
    args:
        text: element to be detected
    '''
    # Search the function by key in the json
    f = open('configuration'+sep+element_trace)
    json_func = json.load(f)
    return json_func[text]

def select_random_list(objects):
    '''
    Selecting a ramdom object of a list
    args:
        objects: elist of objects
    '''
    index = random.randint(0,len(objects)-1)      
    return objects[index]
