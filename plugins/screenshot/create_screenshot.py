import random
import time
import random
import os
import shutil
import tools.generic_utils as util

def generate_screenshot_demo(list):
    '''
    Generate a string with an extension png
    '''
    # Random number and the extension with a img identification
    generate_path = list[0]
    number = list[1]
    return generate_path+str(number)+"_img.png"

def change_screenshot_name(list):
    '''
    Generate an image copy renamed
    '''
    capture = list[0]
    generate_path = list[1]
    number = list[2]
    name = generate_path+number+"_img.png"
    shutil.copyfile(capture, name)
    # Random number and the extension with a img identification
    return name

def generate_capture(columns_ui,columns,element,acu,generate_path,attr):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        acu: number of the case
        variante: if use the initial value or the generate
    '''    
    pathA = os.getcwd()
    capturePath= element["initValue"]
    args_tmp = element["args"]
    list = [generate_path,acu]
    for i in columns_ui:
        try:
            new_image = generate_screenshot_demo(list)
            arguments = []
            if "TextInput" in columns and i == "TextInput":
                ind_text = columns.index("TextInput")
                text = attr[ind_text]
                arguments.append(text)
            func = args_tmp[i]
            for j in func:
                if element is not None:
                    coordinates = j["coordinates"]
                    name = j["name"]
                    args = j["args"]
                    if os.path.exists(pathA+"\\"+new_image):
                        capturePath=new_image
                    arguments.append(args)
                    arguments.append(new_image)
                    arguments.append(capturePath)
                    arguments.append(coordinates)
                    val = util.detect_function(name)(arguments)
                    #list = [capturePath,generate_path,acu]
                    #val = change_screenshot_name(list) 
                else:
                    val="NaN"
                arguments = []
        except:
            new_image = "NaN"
    return new_image