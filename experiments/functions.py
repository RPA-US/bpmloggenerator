import csv
import os
import sys
import time
import json
import random
import json
from colorama import Back,Style, Fore
from plugins.screenshot.create_screenshot import generate_capture, generate_scenario_capture
from plugins.screenshot.replace_gui_component import generate_copied_capture_without_root, generate_copied_capture
from agosuirpa.generic_utils import detect_function
from configuration.settings import sep, scenario_size

def validation_params(json,generate_path,number_logs,percent_per_trace):   
    '''
    Validate the user inputs
    args:
        json: json generated with the trace
        generate_path: log generation destination path
        number_logs: number of log case to generate
        percent_per_trace: percentage of cases for the two possible json traces
    '''
    # actual_path = os.getcwd()
    if (len(percent_per_trace) >= 2) and (number_logs and number_logs > 0) and generate_path != "":
        res = True
    else:
        res = False
    return res



def generate_row(generate_path,dict,acu,case,variant, screenshot_column_name, screenshot_name_generation_function,experiment):
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
                            val = generate_capture(experiment, columns_ui,columns,element,acu,case,generate_path,attr, key, variant, screenshot_name_generation_function)
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
    all_zero = True
    for l in list_percents:
        if l != 0:
            all_zero = False
            break
    if all_zero:
        list_percents = [1]
    return list_percents

def case_generation(json_log,generate_path,number_logs,percent_per_trace, activity_column_name, variant_column_name, case_column_name, screenshot_column_name, screenshot_name_generation_function, path, experiment):
    '''
    The main function to generate logs for a case
        args:
            json_path: path of the json generated with the trace
            generate_path: log generation destination path
            number_logs: number of log case to generate
            percent_per_trace: percentage of cases for the two possible json traces
    '''
    if validation_params(json_log,generate_path,number_logs[1],percent_per_trace):
        # json_log = open(json_log_path)
        # json_act_path = json.load(json_log)
        json_act_path = json_log
     
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
            rows,acu = generate_row(generate_path,json_act_path,acu,case,variant,screenshot_column_name, screenshot_name_generation_function,experiment)
            case += 1
            for row in rows:
                writer.writerow(row)
        f.close()
'''        else:
            logging.warning("Configuration arguments are wrongs")
    except:
        logging.warning("Json structure")'''

def automatic_experiments(generate_path, activity_column_name, variant_column_name, case_column_name, screenshot_column_name, balance, size_secuence, variability_conf, scenario, screenshot_name_generation_function,experiment, folder_name):
    if scenario:
        version_path = generate_path + sep + scenario
    else: 
        version_path = generate_path + sep + "version"+str(round(time.time() * 1000))
        os.makedirs(version_path)
    
    # os.system("cd " + param_path_log_generator)
    for i in size_secuence:
        for b in balance:
            size = ['log_size',i]
            output_path = version_path + sep + folder_name + "_" + str(i) + "_" + b + sep
            case_generation(variability_conf, generate_path, size, balance[b], activity_column_name, variant_column_name, case_column_name, screenshot_column_name, screenshot_name_generation_function, output_path,experiment)
    return version_path


def scenario_generation(scenarios_conf, 
                        generate_path, 
                        scenario_size, 
                        colnames, 
                        variability_conf,
                        autogeneration_conf, 
                        screenshot_name_generation_function,
                        experiment):
    folder_name=experiment.name
    activity_column_name = colnames["Activity"]
    variant_column_name = colnames["Variant"]
    case_column_name = colnames["Case"]
    screenshot_column_name = colnames["Screenshot"]
    prefix_scenario = "scenario_"
    
    if folder_name:
        version_subpath = folder_name+str(round(time.time() * 1000))
    else:
        version_subpath = "version"+str(round(time.time() * 1000))
    database_name = prefix_scenario + version_subpath

    # We established a common path to store all scenarios information 
    path = generate_path + sep + "resources" + sep + version_subpath
    if not os.path.exists(path):
        os.makedirs(path)
    
    
    # Scenario variability: screenshot seeds to later generate case variability are generated 
    image_names_conf = {}
    # scenario_json = json.load(scenarios_conf)
    scenario_json = scenarios_conf
    
    n_scenario_seed_logs = []
    image_mapping = {}
    # Call scenario variation: "size" variations 
    for scenario_i in range(0, scenario_size+1):
        scenario_iteration_path = prefix_scenario + str(scenario_i)
        image_names_conf[scenario_i] = {}
        # Loading json to modify
        original_json = variability_conf
        
        for variant in range(1,len(list(autogeneration_conf["balance"].values())[0])+1):
            image_names_conf[scenario_i][variant] = {}
            json_list = scenario_json[str(variant)]
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
                            val = generate_scenario_capture(experiment,element,0,generate_path,key,variant,new_image,scenario_i)
                    elif variate == 0:
                        if initValue !="":
                            image_to_duplicate = path + sep + scenario_iteration_path + sep + scenario_iteration_path + "_" + select_last_item(element["image_to_duplicate"],sep)
                            val = generate_copied_capture([image_to_duplicate,path + sep + scenario_iteration_path + sep,scenario_iteration_path + "_" +new_init_value])
                        else:
                            val="NaN"
                    original_json["trace"][str(variant)][key][screenshot_column_name]["initValue"] = str(val)
            
        # Serializing json 
        json_to_write = json.dumps(original_json, indent = 4)
        # Writing to .json
        filename = path + sep + prefix_scenario + str(scenario_i) + "_" + folder_name
        with open(filename, "w") as outfile:
            outfile.write(json_to_write)
        image_mapping = filename
            
        n_scenario_seed_logs.append(image_mapping)
        image_mapping = {}
    # Output will be a list that contains the path of each JSON modified (by scenario and family)
    # n_scenario_seed_logs = [{"Basic": "basic_conf_scenario1.json", "Intermediate": "intermediate_conf_scenario1.json", "Advanced": "advanced_conf_scenario1.json"},
    #   {"Basic": "basic_conf_scenario2.json", "Intermediate": "intermediate_conf_scenario2.json", "Advanced": "advanced_conf_scenario2.json"}, ...
    #   ]
    
    # f = open(generate_path+"log.csv", 'w',newline='')
    # writer = csv.writer(f)
    
    # For each different scenario generate case variability as indicate in "trace" inside "json_case_variability"
    for index, scenario_conf in enumerate(n_scenario_seed_logs):
        print(Fore.GREEN + " Scenario " + str(index))
        print(Style.RESET_ALL)
        automatic_experiments(path, activity_column_name, variant_column_name, case_column_name, screenshot_column_name,  autogeneration_conf["balance"], autogeneration_conf["size_secuence"], scenario_conf, 
                            prefix_scenario+str(index), screenshot_name_generation_function,experiment,folder_name)
        
    return version_subpath#path


def select_last_item(initValue, sep):
    new_init_value = initValue
    if sep in initValue:
        splitted = initValue.split(sep)
        new_init_value = splitted[len(splitted)-1]
    return new_init_value

def execute_experiment(experiment, param_mode, number_scenarios, variability_conf, autogeneration_conf, scenarios_conf, generate_path, special_colnames, screenshot_name_generation_function):
    if param_mode == "unique_scenario":
        database_name = "experiment_"+str(round(time.time() * 1000))+"_"
        foldername = automatic_experiments(generate_path, special_colnames["Activity"], special_colnames["Variant"], special_colnames["Case"],
                              special_colnames["Screenshot"], autogeneration_conf["balance"],
                              autogeneration_conf["size_secuence"], None, screenshot_name_generation_function,experiment)
    else:    
        print(Back.GREEN + experiment.name)
        print(Style.RESET_ALL)
        foldername = scenario_generation(scenarios_conf, 
                                         generate_path, 
                                         number_scenarios, 
                                         special_colnames, 
                                         variability_conf, 
                                         autogeneration_conf, 
                                         screenshot_name_generation_function, 
                                         experiment)
    return foldername