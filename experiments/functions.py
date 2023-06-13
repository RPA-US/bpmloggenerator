import csv
import os
import time
import json
import random
import json
from colorama import Back, Style, Fore
from plugins.screenshot.create_screenshot import generate_capture, generate_scenario_capture
from plugins.screenshot.screenshot_filenames import generate_copied_capture_without_root, generate_copied_capture
from bpmloggenerator.generic_utils import detect_function, args_by_function_in_order
from bpmloggenerator.settings import sep, EXPERIMENT_RESULTS_PATH, UI_LOGS_FOLDERNAME, ADDITIONAL_SCENARIOS_RESOURCES_FOLDERNAME, PREFIX_SCENARIO

def validation_params(json, number_logs, percent_per_trace):
    '''
    Validate the user inputs
    args:
        json: json generated with the trace
        generate_path: log generation destination path
        number_logs: number of log case to generate
        percent_per_trace: percentage of cases for the two possible json traces
    '''
    # actual_path = os.getcwd()
    if (len(percent_per_trace) >= 2) and (number_logs and number_logs > 0):
        res = True
    else:
        res = False
    return res


def generate_row(experiment, generate_path, dict, acu, case, variant, original_experiment, balanced, log_size):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        acu: number of the case
        variante: if use the initial value or the generate
    '''
    screenshot_column_name = experiment.special_colnames["Screenshot"]
    attachments_path = experiment.screenshots_path

    rows = []
    columns = dict["columnsNames"]
    columns_ui = dict["GUIElements"]
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
                    args = args_by_function_in_order(element["args"], name)
                    if variate == 1:
                        if i == screenshot_column_name:
                                val = generate_capture(
                                    experiment, columns_ui, columns, element, acu, case, generate_path, attr, key, variant, attachments_path, balanced, log_size, original_experiment)
                        else:
                            val = detect_function(name)(args)
                    elif variate == 0:
                        if initValue != "":
                            if i == screenshot_column_name:
                                if original_experiment:
                                    initValue = attachments_path + sep + initValue
                                val = generate_copied_capture_without_root({
                                    "original_image_path": initValue, 
                                    "image_path_to_save": generate_path, 
                                    "number_to_concatenate": acu
                                    })
                            else:
                                val = initValue
                        else:
                            val = ""
                    # print("Varying " + str(variant) + "-act." + str(key))
                else:
                    val = ""
            attr.append(val)
        rows.append(tuple([case, key, variant] + attr))
    return rows, acu


def number_rows_by_cases(number_logs, percent_per_trace):
    list_percents = []
    total_percent = 0
    # Calculate the number of cases per trace with the percent per case
    for i in range(0, len(percent_per_trace)):
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
    for i in range(0, len(percent_per_trace)):
        num_of_activities = len(dict[str(i+1)])
        # The number of cases is rounded
        trace_percent = round(
            (percent_per_trace[i]*number_logs)/num_of_activities)
        print("=======================================\nVariant "+str(i+1) +
              ":\n  Number of activities -> "+str(num_of_activities) +
              "\n  Percentage indicated -> "+str(percent_per_trace[i]) +
              "\n  Cases generated      -> "+str(trace_percent))
        list_percents.append(trace_percent)
    # normalised_vector = [i/sum(list_percents) for i in list_percents]
    all_zero = True
    for l in list_percents:
        if l != 0:
            all_zero = False
            break
    if all_zero:
        list_percents = [1]
    return list_percents


def case_generation(experiment, json_log, generate_path, number_logs, percent_per_trace, path, original_experiment, balanced, number_executions, current_execution):
    '''
    The main function to generate logs for a case
        args:
            json_path: path of the json generated with the trace
            generate_path: log generation destination path
            number_logs: number of log case to generate
            percent_per_trace: percentage of cases for the two possible json traces
    '''
    generate_path = path
    activity_column_name = experiment.special_colnames["Activity"]
    variant_column_name = experiment.special_colnames["Variant"]
    case_column_name = experiment.special_colnames["Case"]

    if validation_params(json_log, number_logs[1], percent_per_trace):
        if number_logs[0] == "log_size":
            list_percents = number_rows_by_number_of_activities(
                json_log["trace"], number_logs[1], percent_per_trace)
        else:
            list_percents = number_rows_by_cases(
                number_logs[1], percent_per_trace)

        # Generate directory to storage screenshots and log generated
        if path:
            generate_path = path
        else:
            generate_path += sep+str(round(time.time() * 1000))+"logs"+sep
        if not os.path.exists(generate_path):
            os.makedirs(generate_path)

        # Generate CSV
        f = open(generate_path+"log.csv", 'w', newline='')

        writer = csv.writer(f)
        columns = [case_column_name, activity_column_name,
                   variant_column_name] + json_log["columnsNames"]
        writer.writerow(tuple(columns))
        acu = 0
        case = 1
        total_variants = []
        for i, num_cases_per_variant_i in enumerate(list_percents):
            total_variants += num_cases_per_variant_i * [i+1]

        random.shuffle(total_variants)
        total = len(total_variants)
        # TODO: control exception in case: number_executions<=1
        current_percentage = current_execution / number_executions
        advance_range = ((current_execution + 1) / number_executions) - current_percentage
        for i, variant in enumerate(total_variants):
            rows, acu = generate_row(experiment,
                                     generate_path, json_log, acu, case, variant, original_experiment, balanced, number_logs[1])
            case += 1
            print("\n =>  "+str(((i/total * advance_range) + current_percentage)*100)+" per cent generated")
            experiment.is_being_processed = int(((i/total * advance_range) + current_percentage)*100)
            experiment.save()
            for row in rows:
                writer.writerow(row)
        f.close()


'''        else:
            logging.warning("Configuration arguments are wrongs")
    except:
        logging.warning("Json structure")'''


def automatic_experiments(experiment, generate_path, variability_conf, scenario):
    balance = experiment.size_balance["balance"]
    size_secuence = experiment.size_balance["size_secuence"]
    total_case_generations = len(size_secuence) * len(balance['Balanced']) 
    current_execution = 0
    
    if scenario > 0:
        current_execution += total_case_generations*scenario
        
        original_experiment = False
        version_path = generate_path + sep + PREFIX_SCENARIO + str(scenario+1)
        json_log = open(variability_conf)
        json_act_path = json.load(json_log)
    else:
        original_experiment = True
        json_act_path = experiment.variability_conf
        version_path = generate_path + sep + "sc_0"
        # os.makedirs(version_path)

    if scenario > -1:
        total_case_generations *= experiment.number_scenarios+1
    
    # os.system("cd " + param_path_log_generator)
    for i in size_secuence:
        for bal_imb in balance:
            size = ['log_size', i]
            output_path = version_path + "_size" + str(i) + "_" + bal_imb + sep
            case_generation(experiment, json_act_path, generate_path,
                            size, balance[bal_imb], output_path, original_experiment,bal_imb,total_case_generations,current_execution)
            current_execution+=1
    return version_path


def select_last_item(initValue, sep):
    new_init_value = initValue
    if sep in initValue:
        splitted = initValue.split(sep)
        new_init_value = splitted[len(splitted)-1]
    return new_init_value


def execute_experiment(experiment):
    scenario_size = experiment.number_scenarios
    variability_conf = experiment.variability_conf
    scenarios_conf = experiment.scenarios_conf
    attachments_path = experiment.screenshots_path
    generate_path = EXPERIMENT_RESULTS_PATH
    screenshot_column_name = experiment.special_colnames["Screenshot"]
    folder_name = experiment.name.replace(" ", "_")+"_"+str(experiment.id)

    print(Back.GREEN + experiment.name)
    print(Style.RESET_ALL)

    # We established a common path to store all scenarios information
    experiment_path = generate_path + sep + \
        folder_name + "_" + str(experiment.id)
    resources_folder = experiment_path + sep + \
        ADDITIONAL_SCENARIOS_RESOURCES_FOLDERNAME
    if not os.path.exists(experiment_path):
        os.makedirs(experiment_path)
    path = experiment_path + sep + UI_LOGS_FOLDERNAME
    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)

    # Original Experiment Generation
    print(Fore.GREEN + "=> Original Experiment")
    print(Style.RESET_ALL)
    
    if scenario_size > 0:
        automatic_experiments(experiment, path, experiment.variability_conf, 0)
    else:
        automatic_experiments(experiment, path, experiment.variability_conf, -1)

    # Addtional Scenarios Generation
    if scenario_size > 0:
        # Scenario variability: screenshot seeds to later generate case variability are generated
        image_names_conf = {}
        # scenario_json = json.load(scenarios_conf)
        scenario_json = scenarios_conf

        n_scenario_seed_logs = []
        image_mapping = {}
        # Call scenario variation: "size" variations
        for scenario_i in range(1, scenario_size+1):
            scenario_iteration_path = PREFIX_SCENARIO + str(scenario_i)
            image_names_conf[scenario_i-1] = {}
            # Loading json to modify
            original_json = variability_conf

            for variant in range(1, len(list(experiment.size_balance["balance"].values())[0])+1):
                image_names_conf[scenario_i-1][variant] = {}
                json_list = scenario_json[str(variant)]
                for key in json_list:
                    element = json_list[key][screenshot_column_name]
                    if element is not None:
                        initValue = element["initValue"]
                        variate = element["variate"]

                        image_prefix = resources_folder + sep + scenario_iteration_path + "_"
                        init_value_original_screenshot = select_last_item(
                            initValue, sep)

                        if variate == 1:
                            val = generate_scenario_capture(
                                experiment, element, 0, generate_path, key, variant, image_prefix + init_value_original_screenshot, scenario_i, attachments_path)
                        elif variate == 0:
                            if initValue != "":
                                image_to_duplicate = image_prefix + \
                                    select_last_item(
                                        element["image_to_duplicate"], sep)
                                val = generate_copied_capture({
                                    "original_image_path": image_to_duplicate, 
                                    "image_path_to_save": resources_folder + sep, 
                                    "to_concatenate": scenario_iteration_path + "_" + init_value_original_screenshot
                                })
                            else:
                                val = ""
                        original_json["trace"][str(variant)][key][screenshot_column_name]["initValue"] = str(val)

            # Serializing json
            json_to_write = json.dumps(original_json, indent=4)
            # Writing to .json
            filename = resources_folder + sep + \
                PREFIX_SCENARIO + str(scenario_i) + ".json"
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
            print(Fore.GREEN + "\n=> Additional Scenario " + str(index+1))
            print(Style.RESET_ALL)
            automatic_experiments(experiment, path, scenario_conf, index+1)

    return experiment_path
