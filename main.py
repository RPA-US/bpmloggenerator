import csv
import os
import logging
import sys
import time
import json
from plugins.screenshot.create_screenshot import generate_capture
from plugins.screenshot.replace_gui_component import generate_copied_capture
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



def generate_row(generate_path,dict,acu,variant, screenshot_column_name, case):
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
                            val = generate_capture(columns_ui,columns,element,acu,generate_path,attr, case, key, variant)
                        else:
                            val  = detect_function(name)(args)
                    elif variate == 0:
                        if initValue !="":
                            if i==screenshot_column_name:
                                val = generate_copied_capture([initValue,generate_path,acu])
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

def case_generation(json_log_path,generate_path,number_logs,percent_per_trace, activity_column_name, variant_column_name, case_column_name, screenshot_column_name, path):
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
        # TODO: randommize the order of V1 case and others
        for index, num_cases in enumerate(list_percents):
            for i in range(1,num_cases+1):
                rows,acu = generate_row(generate_path,json_act_path,acu,index+1,screenshot_column_name,case)
                case+=1
                for row in rows:
                    writer.writerow(row)
        f.close()
'''        else:
            logging.warning("Configuration arguments are wrongs")
    except:
        logging.warning("Json structure")'''

def automatic_experiments(json_log_path, generate_path, activity_column_name, variant_column_name, case_column_name, screenshot_column_name, balanced, imbalanced, size_secuence, families):
    # Specify balanced and imbalanced percentage to automatic generation of experiments
    balance_conf = {
        "Balanced": balanced,
        "Imbalanced": imbalanced
    }
    
    version_path = generate_path + sep + "version"+str(round(time.time() * 1000))
    os.makedirs(version_path)
    
    # os.system("cd " + param_path_log_generator)
    for family in families:
        for i in size_secuence:
            for b in balance_conf:
                size = ['log_size',i]
                output_path = version_path + sep + family + "_" + str(i) + "_" + b + sep
                case_generation(json_log_path,generate_path,size,balance_conf[b], activity_column_name, variant_column_name, case_column_name, screenshot_column_name, output_path)

def scenario_generation(json_case_variability, generate_path, size, label_division, colnames):
    activity_column_name = colnames["Activity"]
    variant_column_name = colnames["Variant"]
    case_column_name = colnames["Case"]
    screenshot_column_name = colnames["Screenshot"]
    # Scenario variability: screenshot seeds to later generate case variability are generated 
    
    # For each different scenario generate case variability as indicate in "trace" inside "json_case_variability"
    

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
    param_mode = sys.argv[1] if len(sys.argv) > 1 else "normal_mode"
    json_log_path = sys.argv[2] if len(sys.argv) > 2 else "resources"+sep+"Json_capture.json"
    number_logs = list(sys.argv[3]) if len(sys.argv) > 3 else ["log_size",10]
    percent_per_trace = list(sys.argv[4]) if len(sys.argv) > 4 else [0.5,0.5]
    generate_path = sys.argv[5] if len(sys.argv) > 5 else "CSV_exit"
    
    default_conf = { 
        "balanced": [0.5,0.5],
        "imbalanced": [0.1,0.9],
        # Specify secuence of log sizes to automatic generation of experiments
        "size_secuence": [10, 100],#,100,1000]
        "families": ["Basic"]#, "Intermediate", "Advanced"]
    }
    autogeneration_conf = sys.argv[6] if len(sys.argv) > 6 else default_conf
    scenario_size = sys.argv[7] if len(sys.argv) > 7 else 10

    
    colnames = {
        "Case": "Case",
        "Activity": "Activity",
        "Screenshot": "Screenshot",
        "Variant": "Variant"
    }
    special_colnames = sys.argv[7] if len(sys.argv) > 7 else colnames # It must coincide with the column in the seed log
    
    if param_mode == "autogeneration_mode":
        # To use this mode execute: python main.py autogeneration_mode
        # TODO: autogeneration_conf JSON parse (not autogeneration_conf situation) 
        automatic_experiments(json_log_path, generate_path, special_colnames["Activity"], special_colnames["Variant"], special_colnames["Case"],
                              special_colnames["Screenshot"], autogeneration_conf["balanced"], autogeneration_conf["imbalanced"],
                              autogeneration_conf["size_secuence"], autogeneration_conf["families"])
    elif param_mode == "autoscenario_mode":
        size = {
            number_logs,
            scenario_size
        }
        scenario_generation(json_log_path, generate_path, size, percent_per_trace, colnames)
    else:
        case_generation(json_log_path,generate_path,number_logs,percent_per_trace, special_colnames["Activity"], 
                        special_colnames["Variant"], special_colnames["Case"], special_colnames["Screenshot"], None)


