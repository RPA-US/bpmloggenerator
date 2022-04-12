import json
import random
import os
from agosuirpa.system_configuration import function_trace, element_trace
import os
from wizard.models import VariabilityFunction, FunctionParam

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

def args_by_function_in_order(list_dict,name,spec=False):
    argsList = []
    try:        
        if(name=="replace_gui_element_various_places"):
            for i in list_dict:
                argsList = (list_dict[i])
        else:
            if not(name =="" or len(list_dict)==0):
                function_name = VariabilityFunction.objects.get(id_code=name)
                function_params = FunctionParam.objects.filter(variability_function=function_name).order_by("order")  
                #TODO: use the validation attribute            
                if(len(list_dict) == len(function_params)):
                    for i in function_params:
                        if type(list_dict[i.id_code]) is list:
                            for j in list_dict[i.id_code]:
                                argsList.append(j)
                        else:
                            argsList.append(list_dict[i.id_code])
    except:
        argsList=[]
    return argsList
