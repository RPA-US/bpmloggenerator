import os
import agosuirpa.generic_utils as util
from experiments.models import Variations
from agosuirpa.generic_utils import detect_function
from agosuirpa.settings import sep
import ast

def manage_dependency(experiment, name, arguments, argumentsSave, j, case, scenario, activity, variant, balanced, log_size, image_path_to_save, capture_path, coordinates):
    if "args_dependency" in j:
        dependant_row = Variations.objects.filter(experiment=experiment, case_id=case, scenario=scenario, balanced=balanced, log_size=log_size,
                                               activity=j["args_dependency"]["Activity"], case_variation_id=j["args_dependency"]["id"], variant=j["args_dependency"]["V"]).order_by("id")
        row=dependant_row[len(dependant_row)-1]
        tmp = ast.literal_eval(row.arguments)
        arguments = tmp+arguments
        name=row.function_name
        if len(arguments) > 0:
            arguments[0].insert(0, row.result)
        else:
            arguments.append(row.result)
            
    image_element = util.detect_function(name)(arguments)
    if type(image_element) == str:
        Variations.objects.create(experiment=experiment, case_id=case, scenario=scenario, balanced=balanced, log_size=log_size,
                                  case_variation_id=j["id"], activity=activity, variant=variant, function_name=name, arguments=argumentsSave, result=image_element, image_path_to_save=image_path_to_save, capture_path=capture_path, coordinates=coordinates)


def generate_capture(experiment, columns_ui, columns, element, acu, case, generate_path, attr, activity, variant, attachments_path, balanced, log_size, original_experiment):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        case: number of the case
        variante: if use the initial value or the generate
    '''
    # actual_path = os.getcwd()
    if original_experiment:
        capture_path = attachments_path + sep + element["initValue"]
    else:
        capture_path = element["initValue"]
    args_tmp = element["args"]
    args = [generate_path, acu]
    #new_image = generate_screenshot_demo(args)
    new_image = detect_function(
        experiment.screenshot_name_generation_function)(args)
    try:
        for i in columns_ui:
            try:
                arguments = []
                if i in args_tmp:
                    func = args_tmp[i]
                    for j in func:
                        print(j['id'])
                        if element is not None:
                            coordinates = j["coordinates"]
                            name = j["name"]
                            #TODO: generate autocolumns in front and edit this line
                            if not "args_dependency" in j: 
                                if experiment.screenshot_name_generation_function == "insert_text_image" and i in columns or "TextInput" in columns:
                                    arguments.append(attr[columns.index(i)])
                                args = util.args_by_function_in_order(j["args"],name)
                                arguments.append(args)
                            if not sep in new_image:
                                image_path_to_save = generate_path + new_image
                            else:
                                image_path_to_save = new_image

                            # Check if there are previous variations applied to the original image and substitute the original image path by the modified one
                            if os.path.exists(image_path_to_save):
                                capture_path = image_path_to_save

                            argumentsSave = arguments.copy()
                            arguments.append(image_path_to_save)
                            arguments.append(capture_path)
                            arguments.append(coordinates)

                            manage_dependency(experiment, name, arguments, argumentsSave, j, case, 0, 
                                              activity, variant, balanced, log_size, image_path_to_save, capture_path, coordinates)
                        else:
                            new_image = ""
                        arguments = []
            except Exception as e:
                # print("Unexpected error: " + str(e)) // TODO
                arguments = []
    except Exception as e:
        print("Unexpected error: " + str(e))
        # func = args_tmp[i] or content = attr[ind_text]: list out of range
        new_image = ""
    return new_image


def generate_scenario_capture(experiment, element, case, generate_path, activity, variant, new_image, scenario, attachments_path):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        case: number of the case
        variante: if use the initial value or the generate
    '''
    capture_path = attachments_path + sep + element["initValue"]
    json_args = element["args"]
    args = [generate_path, case]

    arguments = []
    for gui_component_label in json_args:
        for variation_conf in json_args[gui_component_label]:
            if element is not None:
                coordinates = variation_conf["coordinates"]
                name = variation_conf["name"]
                if not "args_dependency" in variation_conf: 
                    args = util.args_by_function_in_order(variation_conf["args"],name)
                    arguments.append(args)
                if not sep in new_image:
                    image_path_to_save = generate_path + new_image
                else:
                    image_path_to_save = new_image

                # Check if there are previous variations applied to the original image and substitute the original image path by the modified one
                if os.path.exists(image_path_to_save):
                    capture_path = image_path_to_save

                argumentsSave = arguments.copy()
                arguments.append(image_path_to_save)
                arguments.append(capture_path)
                arguments.append(coordinates)

                manage_dependency(experiment, name, arguments, argumentsSave,
                                  variation_conf, case, scenario, activity, variant, None, None)
            else:
                new_image = ""
            arguments = []

    return new_image
