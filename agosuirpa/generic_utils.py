import json
import random
import os
from agosuirpa.system_configuration import function_trace, element_trace
import os

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
    f = open(function_trace)
    json_func = json.load(f)
    return eval(json_func[text])

def detect_element(text):
    '''
    Selecting an element in the system by means of a keyword
    args:
        text: element to be detected
    '''
    # Search the function by key in the json
    f = open(element_trace)
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