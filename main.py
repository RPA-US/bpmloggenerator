from plugins.string.random_text_lorem import generate_path, generate_paragraph, generate_sentence, generate_words, generate_DNI,generate_random_entity
from plugins.list.coordenates_in_range import generate_mouse_position
from plugins.list.mouse_tipe import generate_mousekeyboard
from plugins.screenshot.replace_gui_component import generate_screenshot_demo
from plugins.app.nameapp import generate_app_demo
from tools.generic_utils import detect_function
import csv
import os
import logging
import time
import json

'''
Validate the user inputs
'''
def validation_params(json_path,generate_path,number_logs,percent_per_traze):
    res = True
    if os.path.exists(json_path):
        res = True
    else:
        return False
    if len(percent_per_traze) == 2:
        res = True
    else:
        return False
    acu = 0
    for i in percent_per_traze:
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

'''
Generate row reading the json
'''
def generate_row(dict,case,variante):
    Timestamp = str(round(time.time() * 1000)+1)
    rows = []
    for key in dict:
        Activity = key
        if dict[key]["MorKeyb"] is not None:
            val = dict[key]["MorKeyb"]
            initValue = val["initValue"]
            variate = val["variate"]
            name = val["name"]
            args = val["args"]
            if initValue  == "":
                MorKeyb = generate_mousekeyboard()
            else:
                MorKeyb = initValue
            if MorKeyb == 1:
                Coor_X,Coor_y = detect_function(name)(args)
            else:
                Coor_X = "NaN"
                Coor_y = "NaN"
        else:
            MorKeyb=""
            Coor_X = "NaN"
            Coor_y = "NaN"
        if dict[key]["TextInput"] is not None:
            val = dict[key]["TextInput"]
            initValue = val["initValue"]    
            variate = val["variate"]
            name = val["name"]
            args = val["args"]
            if initValue =="":
                if args =="":
                    TextInput  = detect_function(name)()
                else:
                    TextInput  = detect_function(name)(args)
            else:
                TextInput = initValue
        else:
            TextInput="NaN"
        if dict[key]["NameApp"] is not None:
            val = dict[key]["NameApp"]
            initValue = val["initValue"]
            variate = val["variate"]
            name = val["name"]
            args = val["args"]
            if initValue =="":
                if args =="":
                    NameApp  = detect_function(name)()
                else:
                    NameApp  = detect_function(name)(args)
            else:
                NameApp = initValue
        else:
            NameApp="NaN"
        if dict[key]["Screenshot"] is not None:
            val = dict[key]["Screenshot"]
            initValue = val["initValue"]
            variate = val["variate"]
            name = val["name"]
            args = val["args"]
            if initValue  =="":
                if args =="":
                    Screenshot  = detect_function(name)()
                else:
                    Screenshot  = detect_function(name)(args)
            else:
                Screenshot = initValue
        else:
            Screenshot="NaN"
        rows.append((Timestamp,str(case),Activity,str(variante),MorKeyb,Coor_X,Coor_y,TextInput,NameApp,Screenshot))
    return rows
    

def main_function(json_path,generate_path,number_logs,percent_per_traze):
    if validation_params(json_path,generate_path,number_logs,percent_per_traze):
        f = open(json_path)
        json_act_path = json.load(f)
        list_percents = []
        total_percent = 0
        for i in range(0,len(percent_per_traze)):
            if i != len(percent_per_traze):
                traze_percent = round(percent_per_traze[i]*number_logs)
                total_percent += traze_percent
                list_percents.append(traze_percent)
            else:
                list_percents.append(number_logs-total_percent)
        if not os.path.exists(generate_path):
            os.mkdir(generate_path)
        f = open(generate_path+"\\"+str(round(time.time() * 1000))+"-generated_logs.csv", 'w')
        writer = csv.writer(f)
        writer.writerow(("Timestamp","Case","Activity","Variant","MorKeyb","Coor_X","Coor_Y","TextInput","NameApp","Screenshot"))
        acu = 0
        for i in range(1,len(list_percents)+1):
            for j in range(0,list_percents[i-1]):
                acu += 1
                rows = generate_row(json_act_path[str(i)],acu,i)
                for row in rows:
                    writer.writerow(row)
        f.close()
    else:
        logging.warn("Configuration arguments are wrongs")
    
        
if __name__ == '__main__':
    json_path = "Json_example.json"
    generate_path = "CSV_sample_exit.csv"
    number_logs = 10
    percent_per_traze = [0.25,0.75]
    main_function(json_path,generate_path,number_logs,percent_per_traze)    

