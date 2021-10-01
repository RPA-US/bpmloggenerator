import json
from plugins.string.random_text_lorem import generate_path, generate_paragraph, generate_sentence, generate_words, generate_DNI,generate_random_entity
from plugins.list.coordenates_in_range import generate_mouse_position, generate_mouse_position_x, generate_mouse_position_y
from plugins.list.mouse_tipe import generate_mousekeyboard
from plugins.screenshot.replace_gui_component import generate_screenshot_demo
from plugins.app.nameapp import generate_app_demo
from plugins.string.random_timestamp import generate_timestamp

'''
Ver que se hace con las funciones
'''
def detect_function(text):
    f = open('function_trace.json')
    json_func = json.load(f)
    return eval(json_func[text])
