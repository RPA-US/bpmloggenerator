import os
import tools.generic_utils as util
from tools.database import create_connection, select_variations_by, create_variation
from tools.generic_utils import detect_function
from configuration.settings import sep

def generate_capture(columns_ui,columns,element,acu,generate_path,attr,case, activity, variant, screenshot_name_generation_function):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        acu: number of the case
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
                            # if os.path.exists(actual_path+sep+new_image):
                            #     capture_path=new_image
                            if not sep in new_image:
                                image_path_to_save = generate_path + new_image
                            else:
                                image_path_to_save = new_image
                            arguments.append(args)
                            arguments.append(image_path_to_save)
                            arguments.append(capture_path)
                            arguments.append(coordinates)
                            if "dependency" in j:
                                con = create_connection()
                                dependant_row = select_variations_by(con, case, j["dependency"]) # fetch a list
                                arguments.append(dependant_row[0][4])
                                
                            image_element = util.detect_function(name)(arguments)
                            if type(image_element) == str:
                                create_variation(None, case, activity, variant, name, image_element)
                        else:
                            new_image="NaN"
                        arguments = []
            except:
                arguments = []
    except:
        new_image = "NaN"
    return new_image