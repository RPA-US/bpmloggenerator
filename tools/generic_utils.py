import json
from plugins.string.random_text_lorem import generate_DNI,generate_paragraph,generate_path,generate_random_entity,generate_sentence,generate_words
from plugins.list.coordenates_in_range import generate_mouse_position, generate_mouse_position_x,generate_mouse_position_y
from plugins.list.mouse_tipe import generate_mousekeyboard
from plugins.screenshot.replace_gui_component import hidden_gui_element, insert_text_image, replace_gui_element_by_other
from plugins.app.nameapp import generate_app_demo
from plugins.string.random_timestamp import generate_timestamp

def detect_function(text):
    '''
    Selecting a function in the system by means of a keyword
    args:
        text: function to be detected
    '''
    # Search the function by key in the json
    f = open('resources\\function_trace.json')
    json_func = json.load(f)
    return eval(json_func[text])

def detect_element(text):
    '''
    Selecting an element in the system by means of a keyword
    args:
        text: element to be detected
    '''
    # Search the function by key in the json
    f = open('resources\\element_trace.json')
    json_func = json.load(f)
    return json_func[text]
