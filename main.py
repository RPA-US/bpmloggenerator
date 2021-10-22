import csv
import os
import logging
import time
import json
from plugins.screenshot.create_screenshot import generate_capture
from tools.generic_utils import detect_function

def validation_params(json_path,generate_path,number_logs,percent_per_trace):   
    '''
    Validate the user inputs
    args:
        json_path: path of the json generated with the trace
        generate_path: log generation destination path
        number_logs: number of log case to generate
        percent_per_trace: percentage of cases for the two possible json traces
    '''
    pathA = os.getcwd()
    res = True
    if os.path.exists(pathA+"\\"+json_path):
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
    return res



def generate_row(generate_path,dict,acu,variante):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        acu: number of the case
        variante: if use the initial value or the generate
    '''
    Timestamp = str(round(time.time() * 1000)+1)
    rows = []
    columns= dict["columnsNames"]
    columns_ui= dict["GUIElements"]
    json_list = dict["trace"][str(variante)]
    for key in json_list:
        attr = []
        acu += 1
        text = ""
        for i in columns:
            element = json_list[key][i]
            if element is not None:
                initValue = element["initValue"]
                variate = element["variate"]
                name = element["name"]
                args = element["args"]
                if variate == 1:
                    if name=="function30":
                        val = generate_capture(columns_ui,columns,element,acu,generate_path,attr)
                    else:
                        val  = detect_function(name)(args)
                elif initValue !="":
                    val = initValue 
                else:
                    val="NaN"
            else:
                val="NaN"
            attr.append(val)
        rows.append(tuple(attr))
    return rows,acu


def main_function(json_log_path,generate_path,number_logs,percent_per_trace):
    '''
    The main function to generate logs
        args:
            json_path: path of the json generated with the trace
            generate_path: log generation destination path
            number_logs: number of log case to generate
            percent_per_trace: percentage of cases for the two possible json traces
    '''
    #try:
    if validation_params(json_log_path,generate_path,number_logs,percent_per_trace):
        f = open(json_log_path)
        json_act_path = json.load(f)
        list_percents = []
        total_percent = 0
        # Calculate the number of cases per trace with the percent per case
        for i in range(0,len(percent_per_trace)):
            # The number of cases is rounded
            if i != len(percent_per_trace):
                trace_percent = round(percent_per_trace[i]*number_logs)
                total_percent += trace_percent
                list_percents.append(trace_percent)
            else:
            # The number of cases for the second trace after rounding
                list_percents.append(number_logs-total_percent)
        generate_path = generate_path+"\\"+str(round(time.time() * 1000))+"logs\\"
        if not os.path.exists(generate_path):
            os.mkdir(generate_path)
        f = open(generate_path+"log.csv", 'w',newline='')
        writer = csv.writer(f)
        columns = json_act_path["columnsNames"]
        writer.writerow(tuple(columns))
        acu = 0
        for i in range(1,len(list_percents)+1):
            for j in range(0,list_percents[i-1]):
                rows,acu = generate_row(generate_path,json_act_path,acu,i)
                for row in rows:
                    writer.writerow(row)
        f.close()
'''        else:
            logging.warning("Configuration arguments are wrongs")
    except:
        logging.warning("Json structure")'''


if __name__ == '__main__':
    json_log_path = "resources\\Json_example_log.json"
    generate_path = "CSV_sample_exit_csv"
    number_logs = 10
    percent_per_trace = [0.25,0.75]
    main_function(json_log_path,generate_path,number_logs,percent_per_trace)
    '''
    from plugins.screenshot.replace_gui_component import insert_text_image, hidden_gui_element
    capture = "resources/Captura de pantalla 2021-10-05 132706.png"
    coordenates = [100,500,150,550]
    new_image = "10_img.png"
    configuration = [(0,0,0)]
    hidden_gui_element(capture, coordenates, new_image, configuration)
    '''
    '''
    from plugins.screenshot.replace_gui_component import insert_text_image, hidden_gui_element
    text = "Hello world!"
    font = "resources/Roboto-Black.ttf"
    font_size = 16
    font_color = "#000000"
    new_image = "10_img.png"
    capture = "Captura de pantalla 2021-10-05 132706.png"
    coordenates = [100,500]
    list = [text, font, font_size,font_color,new_image,capture,coordenates]
    insert_text_image(list)
    '''

