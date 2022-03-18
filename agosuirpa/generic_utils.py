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

def args_by_function_in_order(list_dict,name):
    argsList = []
    function_name = VariabilityFunction.objects.get(id_code=name)
    paramList = []
    #TODO: change to the correct param order
    function_params = function_name.params.all().order_by("id")
    for i in function_params:
        parTMP = FunctionParam.objects.get(pk=i.id)
        paramList.append(parTMP)
    if(len(list_dict) == len(paramList)):
        for i in paramList:
            argsList.append(list_dict[i.label])
    return argsList
