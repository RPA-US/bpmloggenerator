import os
import agosuirpa.generic_utils as util
from experiments.models import Variations
from agosuirpa.generic_utils import detect_function
from configuration.settings import sep

def manage_dependency(experiment, name, arguments, j, case, scenario, activity, variant):
    if "dependency" in j:
        dependant_row = Variations.objects.get(experiment=experiment, case_id=case, scenario=scenario, activity=j["dependency"]["Activity"], case_variation_id=j["dependency"]["id"], variant=j["dependency"]["V"])
        arguments.append(dependant_row[0][6])                                
    image_element = util.detect_function(name)(arguments)
    if type(image_element) == str:
        Variations.objects.create(experiment=experiment, case_id=case, scenario=scenario, case_variation_id=j["id"], activity=activity, variant=variant, function_name=name, gui_element=image_element)

def generate_capture(experiment, columns_ui,columns,element,acu,case,generate_path,attr, activity, variant, screenshot_name_generation_function):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        case: number of the case
        variante: if use the initial value or the generate
    '''    
    # actual_path = os.getcwd()
    capture_path= element["initValue"]
    args_tmp = element["args"]
    args = [generate_path,acu]
    #new_image = generate_screenshot_demo(args)
    new_image = detect_function(screenshot_name_generation_function)(args)
    try:
        for i in columns_ui:
            try:
                arguments = []
                if i in columns:
                    ind_text = columns.index(i)
                    content = attr[ind_text]
                    arguments.append(content)
                if i in args_tmp:
                    func = args_tmp[i]
                    for j in func:
                        if element is not None:
                            coordinates = j["coordinates"]
                            name = j["name"]
                            args = j["args"]
                            if not sep in new_image:
                                image_path_to_save = generate_path + new_image
                            else:
                                image_path_to_save = new_image
                                
                            # Check if there are previous variations applied to the original image and substitute the original image path by the modified one
                            if os.path.exists(image_path_to_save):
                                capture_path=image_path_to_save
                                
                            arguments.append(args)
                            arguments.append(image_path_to_save)
                            arguments.append(capture_path)
                            arguments.append(coordinates)
                            
                            manage_dependency(experiment, name, arguments, j, case, 0, activity, variant)
                        else:
                            new_image="NaN"
                        arguments = []
            except Exception as e:
                # print("Unexpected error: print in create_screenshot.py line 62")
                # print(e)
                arguments = []
    except Exception as e:
        print("Unexpected error: print in create_screenshot.py line 66")
        # func = args_tmp[i] or content = attr[ind_text]: list out of range
        print(e)
        new_image = "NaN"
    return new_image

def generate_scenario_capture(experiment,element,case,generate_path,activity,variant,new_image,scenario):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        case: number of the case
        variante: if use the initial value or the generate
    '''
    capture_path= element["initValue"]
    json_args = element["args"]
    args = [generate_path,case]

    arguments = []
    for gui_component_label in json_args:
        for variation_conf in json_args[gui_component_label]:
            if element is not None:
                coordinates = variation_conf["coordinates"]
                name = variation_conf["name"]
                args = variation_conf["args"]
                if not sep in new_image:
                    image_path_to_save = generate_path + new_image
                else:
                    image_path_to_save = new_image
                    
                # Check if there are previous variations applied to the original image and substitute the original image path by the modified one
                if os.path.exists(image_path_to_save):
                    capture_path=image_path_to_save
                    
                arguments.append(args)
                arguments.append(image_path_to_save)
                arguments.append(capture_path)
                arguments.append(coordinates)
                
                manage_dependency(experiment, name, arguments, variation_conf, case, scenario, activity, variant)
            else:
                new_image="NaN"
            arguments = []
    
    return new_image