import csv
import os
import logging
from sqlite3.dbapi2 import version
import sys
import time
import json
import random
import json
from plugins.screenshot.create_screenshot import generate_capture, generate_scenario_capture
from plugins.screenshot.replace_gui_component import generate_copied_capture_without_root, generate_copied_capture
from tools.generic_utils import detect_function
from tools.database import init_database
from configuration.settings import sep

def validation_params(json_path,generate_path,number_logs,percent_per_trace):   
    '''
    Validate the user inputs
    args:
        json_path: path of the json generated with the trace
        generate_path: log generation destination path
        number_logs: number of log case to generate
        percent_per_trace: percentage of cases for the two possible json traces
    '''
    actual_path = os.getcwd()
    res = True
    if os.path.exists(actual_path+ sep +json_path):
        res = True
    else:
        return False
    if len(percent_per_trace) == 2:
        res = True
    else:
        return False
    acu = 0
    for i in percent_per_trace:
        acu += i
    if acu == 1:
        res = True
    else:
        return False
    if number_logs > 0 and number_logs:
        res = True
    else:
        return False
    if generate_path == "":
        res = True
    return res



def generate_row(generate_path,dict,acu,case,variant, screenshot_column_name, screenshot_name_generation_function):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        acu: number of the case
        variante: if use the initial value or the generate
    '''
    rows = []
    columns= dict["columnsNames"]
    columns_ui= dict["GUIElements"]
    json_list = dict["trace"][str(variant)]
    
    for key in json_list:
        attr = []
        acu += 1
        for i in columns:
            if i in json_list[key]:
                element = json_list[key][i]
                if element is not None:
                    initValue = element["initValue"]
                    variate = element["variate"]
                    name = element["name"]
                    args = element["args"]
                                        
                    if variate == 1:
                        if i==screenshot_column_name:
                            val = generate_capture(columns_ui,columns,element,acu,case,generate_path,attr, key, variant, screenshot_name_generation_function)
                        else:
                            val = detect_function(name)(args)
                    elif variate == 0:
                        if initValue !="":
                            if i==screenshot_column_name:
                                val = generate_copied_capture_without_root([initValue,generate_path,acu])
                            else:
                                val = initValue 
                        else:
                            val="NaN"
                else:
                    val="NaN"
            attr.append(val)
        rows.append(tuple([case,key,variant] + attr))
    return rows,acu

def number_rows_by_cases(number_logs, percent_per_trace):
    list_percents = []
    total_percent = 0
    # Calculate the number of cases per trace with the percent per case
    for i in range(0,len(percent_per_trace)):
        # The number of cases is rounded
        if i != len(percent_per_trace)-1:
            trace_percent = round(percent_per_trace[i]*number_logs)
            total_percent += trace_percent
            list_percents.append(trace_percent)
        else:
        # The number of cases for the second trace after rounding
            list_percents.append(number_logs-total_percent)
    return list_percents

def number_rows_by_number_of_activities(dict, number_logs, percent_per_trace):
    list_percents = []
    # Calculate the number of cases per trace with the percent per case
    for i in range(0,len(percent_per_trace)):
        num_of_activities = len(dict[str(i+1)])
        # The number of cases is rounded
        trace_percent = round((percent_per_trace[i]*number_logs)/num_of_activities)
        print("=======================================\nVariant "+str(i+1)+
            ":\n  Number of activities -> "+str(num_of_activities)+
             "\n  Percentage indicated -> "+str(percent_per_trace[i]) +
             "\n  Cases generated      -> "+str(trace_percent))
        list_percents.append(trace_percent)
    #normalised_vector = [i/sum(list_percents) for i in list_percents]
    return list_percents

def case_generation(json_log_path,generate_path,number_logs,percent_per_trace, activity_column_name, variant_column_name, case_column_name, screenshot_column_name, screenshot_name_generation_function, path):
    '''
    The main function to generate logs for a case
        args:
            json_path: path of the json generated with the trace
            generate_path: log generation destination path
            number_logs: number of log case to generate
            percent_per_trace: percentage of cases for the two possible json traces
    '''
    #try:
    if validation_params(json_log_path,generate_path,number_logs[1],percent_per_trace):
        init_database()
        json_log = open(json_log_path)
        json_act_path = json.load(json_log)
     
        if number_logs[0] == "log_size":
            list_percents = number_rows_by_number_of_activities(json_act_path["trace"], number_logs[1], percent_per_trace)
        else:
            list_percents = number_rows_by_cases(number_logs[1],percent_per_trace)
        
        # Generate directory to storage screenshots and log generated
        if path:
            generate_path = path
        else:
            generate_path += sep+str(round(time.time() * 1000))+"logs"+sep
        if not os.path.exists(generate_path):
            os.makedirs(generate_path)
        f = open(generate_path+"log.csv", 'w',newline='')

        writer = csv.writer(f)
        columns = [case_column_name, activity_column_name, variant_column_name] + json_act_path["columnsNames"]
        writer.writerow(tuple(columns))
        acu = 0
        case = 1
        total_variants = []
        for i, num_cases_per_variant_i in enumerate(list_percents):
            total_variants += num_cases_per_variant_i * [i+1]
    
        random.shuffle(total_variants)
        for variant in total_variants:
            rows,acu = generate_row(generate_path,json_act_path,acu,case,variant,screenshot_column_name, screenshot_name_generation_function)
            case += 1
            for row in rows:
                writer.writerow(row)
        f.close()
'''        else:
            logging.warning("Configuration arguments are wrongs")
    except:
        logging.warning("Json structure")'''

def automatic_experiments(generate_path, activity_column_name, variant_column_name, case_column_name, screenshot_column_name, balance, size_secuence, families, scenario, screenshot_name_generation_function):
    if scenario:
        version_path = generate_path + sep + scenario
    else: 
        version_path = generate_path + sep + "version"+str(round(time.time() * 1000))
        os.makedirs(version_path)
    
    # os.system("cd " + param_path_log_generator)
    for family in families.keys():
        for i in size_secuence:
            for b in balance:
                size = ['log_size',i]
                output_path = version_path + sep + family + "_" + str(i) + "_" + b + sep
                case_generation(families[family], generate_path, size, balance[b], activity_column_name, variant_column_name, case_column_name, screenshot_column_name, screenshot_name_generation_function, output_path)

# def refactor_json_image_path(image_mapping, variation_json_seed_per_family, scenario):
#     # After that, we modify each JSON of autogeneration_conf["families"]. Substitution of original image name by variation image name
#     conf = {}
#     for family in image_mapping:
#         for variant in image_mapping[family]:
#             json_log = open(variation_json_seed_per_family[family])
#             original_json = json.load(json_log)
#             json_object = {}
#             json_object = json.dumps(original_json[variant], indent = 4)
#             for original, replacement in image_mapping[family][variant].items():
#                 json_object = json_object.replace(original, replacement)
            
#             original_json[variant] = json.loads(json_object)
        
#         # Serializing json 
#         json_to_write = json.dumps(original_json, indent = 4)
#         # Writing to .json
#         filename = scenario+"_"+variation_json_seed_per_family[family]
#         with open(filename, "w") as outfile:
#             outfile.write(json_to_write)
#         conf[family] = filename
#     return conf

def scenario_generation(scenarios_path, generate_path, scenario_size, colnames, autogeneration_conf, screenshot_name_generation_function):
    activity_column_name = colnames["Activity"]
    variant_column_name = colnames["Variant"]
    case_column_name = colnames["Case"]
    screenshot_column_name = colnames["Screenshot"]
    prefix_scenario = "scenario_"
    variation_json_seed_per_family = autogeneration_conf["families"]
    
    init_database()
    
    # We established a common path to store all scenarios information 
    path = generate_path + sep + "resources" + sep + "version"+str(round(time.time() * 1000))
    if not os.path.exists(path):
        os.makedirs(path)
    
    
    # Scenario variability: screenshot seeds to later generate case variability are generated 
    image_names_conf = {}
    json_log = open(scenarios_path)
    scenario_json = json.load(json_log)
    
    n_scenario_seed_logs = []
    image_mapping = {}
    # Call scenario variation: "size" variations 
    for scenario_i in range(0, scenario_size+1):
        scenario_iteration_path = prefix_scenario + str(scenario_i)
        image_names_conf[scenario_i] = {}
        for family in autogeneration_conf["families"]:
            image_names_conf[scenario_i][family] = {}
            # Loading json to modify
            original_json = json.load(open(variation_json_seed_per_family[family]))
            
            for variant in range(1,len(list(autogeneration_conf["balance"].values())[0])+1):
                image_names_conf[scenario_i][family][variant] = {}
                json_list = scenario_json[family][str(variant)]
                for key in json_list:
                    element = json_list[key][screenshot_column_name]
                    if element is not None:
                        initValue = element["initValue"]
                        variate = element["variate"]
                        
                        new_init_value = select_last_item(initValue, sep)
                        
                        new_image = path + sep + scenario_iteration_path + sep + scenario_iteration_path + "_" +new_init_value
                        if not os.path.exists(path + sep + scenario_iteration_path):
                            os.makedirs(path + sep + scenario_iteration_path)
                            
                        if variate == 1:
                                val = generate_scenario_capture(element,0,generate_path,key,variant,new_image,scenario_i)
                        elif variate == 0:
                            if initValue !="":
                                image_to_duplicate = path + sep + scenario_iteration_path + sep + scenario_iteration_path + "_" + select_last_item(element["image_to_duplicate"],sep)
                                val = generate_copied_capture([image_to_duplicate,path + sep + scenario_iteration_path + sep,scenario_iteration_path + "_" +new_init_value])
                            else:
                                val="NaN"
                        # image_names_conf[scenario_i][family][variant][initValue] = str(val)
                        original_json["trace"][str(variant)][key][screenshot_column_name]["initValue"] = str(val)
                
                # json_object = json.dumps(original_json["trace"][str(variant)], indent = 4)
                # for original, replacement in image_names_conf[scenario_i][family][variant].items():
                #     refactored_json = json.dumps(original_json["trace"][str(variant)]).replace(original, replacement)                                 
                # original_json["trace"][str(variant)] = json.loads(refactored_json)
            # Serializing json 
            json_to_write = json.dumps(original_json, indent = 4)
            # Writing to .json
            filename = path + sep + prefix_scenario + str(scenario_i) + "_" + select_last_item(variation_json_seed_per_family[family], sep)
            with open(filename, "w") as outfile:
                outfile.write(json_to_write)
            image_mapping[family] = filename
            
        n_scenario_seed_logs.append(image_mapping)
    # Output will be a list that contains the path of each JSON modified (by scenario and family)
    # n_scenario_seed_logs = [{"Basic": "basic_conf_scenario1.json", "Intermediate": "intermediate_conf_scenario1.json", "Advanced": "advanced_conf_scenario1.json"},
    #   {"Basic": "basic_conf_scenario2.json", "Intermediate": "intermediate_conf_scenario2.json", "Advanced": "advanced_conf_scenario2.json"}, ...
    #   ]
    
    
    # f = open(generate_path+"log.csv", 'w',newline='')
    # writer = csv.writer(f)
    
    # For each different scenario generate case variability as indicate in "trace" inside "json_case_variability"
    for index, scenario_conf in enumerate(n_scenario_seed_logs):
        autogeneration_conf["families"] = scenario_conf
        automatic_experiments(path, activity_column_name, variant_column_name, case_column_name, screenshot_column_name,  autogeneration_conf["balance"], autogeneration_conf["size_secuence"], autogeneration_conf["families"], 
                            prefix_scenario+str(index), screenshot_name_generation_function)


def select_last_item(initValue, sep):
    new_init_value = initValue
    if sep in initValue:
        splitted = initValue.split(sep)
        new_init_value = splitted[len(splitted)-1]
    return new_init_value

if __name__ == '__main__':
    """[Instructions for use]
    
    * param_mode: can be
        -- "normal_mode": generate one log with the varibility specified in json_log_path
        -- "autogeneration_mode": generate several logs, one for each family-balance pair. Families and banlance/imbalance percentage are indicated on code below
        -- "autoscenario_mode": generate variations at scenario level (changing apps environment GUI components), and for each one execute the autogeneration_mode
        
    * json_log_path: JSON file indicating variability specifications. On normal and autogeneration modes they are indicate in "trace" attribute. On autoscenario mode, there are also a "scenario" attribute to indicate scenario variability (it must contains the same activities and cases than "trace" attribute)
    
    * number_logs: it is a list with two attributes. The first one is the mode we want to measure log size and the second one, the size. There are two modes:
        -- "log_size": the number in the second position restrict the number of rows of the log
        -- "cases_size": the number in the second position restrict the number of cases. Each case will have a number of rows associated, so the size of the logs in terms of number of rows will be greater than the number indicated at second position of the list.
        
    * percent_per_trace: it is a list indicating the percentage of cases of each variant (label) that we want to generate in the log
    
    * generate_path: path where the output of the log generator will be stored
    
    * autogeneration_conf: configuration params use in "autogeneration_mode" to generate logs of different sizes (size_secuence) for variations of type of family (families) and balance percentage (balanced, imbalanced)
    
    * scenario_size: number of scenarios to generate when "autoscenario_mode" is selected
    """
    colnames = {
        "Case": "Case",
        "Activity": "Activity",
        "Screenshot": "Screenshot",
        "Variant": "Variant"
    }
    default_conf = { 
        "balance":{
            # "Balanced": [0.5,0.5],
            # "Imbalanced": [0.3,0.7]
        },
        # Specify secuence of log sizes to automatic generation of experiments
        "size_secuence": [10,50,100],#1000]
        "families": {
            "Basic": "resources"+sep+"test_scenarios"+sep+"Basic_Act5_Var2_DesElem2.json",
            # "Intermediate": "resources"+sep+"Intermediate_Act8_Var2_DesElem2.json",
            # "Advanced": "resources"+sep+"Advanced_Act10_Var2_DesElem4.json"
        }
    }
    param_mode =                            sys.argv[1] if len(sys.argv) > 1 else "autogeneration_mode"
    additional_balance =                    list(sys.argv[2]) if len(sys.argv) > 2 else None
    generate_path =                         sys.argv[3] if len(sys.argv) > 3 else "CSV_exit"
    json_log_path =                         sys.argv[4] if len(sys.argv) > 4 else "resources"+sep+"test_scenarios"+sep+"Basic_Act5_Var2_DesElem2.json"  # not relevant for autogeneration/autoscenario mode
    number_logs =                           list(sys.argv[4]) if len(sys.argv) > 5 else ["log_size",10] # not relevant for autogeneration/autoscenario mode
    percent_per_trace =                     list(sys.argv[5]) if len(sys.argv) > 6 else [0.5,0.5] # not relevant for autogeneration/autoscenario mode
    special_colnames =                      sys.argv[6] if len(sys.argv) > 6 else colnames # It must coincide with the column in the seed log
    screenshot_name_generation_function =   sys.argv[7] if len(sys.argv) > 7 else "function25" # Use function8 to obtain complete paths
    autogeneration_conf =                   json.loads(sys.argv[8]) if len(sys.argv) > 8 else default_conf
    scenario_size =                         sys.argv[9] if len(sys.argv) > 9 else 30
    scenarios_path =                        sys.argv[10] if len(sys.argv) > 10 else "resources"+sep+"test_scenarios"+sep+"scenarios.json"
    
    if additional_balance:
        default_conf["Imbalanced"] = additional_balance
    
    if param_mode == "autogeneration_mode":
        # To use this mode execute: python main.py autogeneration_mode
        automatic_experiments(generate_path, special_colnames["Activity"], special_colnames["Variant"], special_colnames["Case"],
                              special_colnames["Screenshot"], autogeneration_conf["balance"],
                              autogeneration_conf["size_secuence"], autogeneration_conf["families"], None, screenshot_name_generation_function)
    elif param_mode == "autoscenario_mode":
        scenario_generation(scenarios_path, generate_path, scenario_size, colnames, autogeneration_conf, screenshot_name_generation_function)
    else:
        case_generation(json_log_path,generate_path,number_logs,percent_per_trace, special_colnames["Activity"], 
                        special_colnames["Variant"], special_colnames["Case"], special_colnames["Screenshot"], screenshot_name_generation_function, None)