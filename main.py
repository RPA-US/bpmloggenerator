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
    columns= dict["columnsNames"]
    json_list = dict["trace"][str(variante)]
    for key in json_list:
        attr = []
        for i in columns:
            element = json_list[key][i]
            if element is not None:
                initValue = element["initValue"]
                variate = element["variate"]
                name = element["name"]
                args = element["args"]
                if variate == 1:
                    if args =="":
                        val  = detect_function(name)()
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
    return rows

def main_function(json_path,generate_path,number_logs,percent_per_traze):
    #try:
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
        f = open(generate_path+"\\"+str(round(time.time() * 1000))+"-generated_logs.csv", 'w',newline='')
        writer = csv.writer(f)
        columns = json_act_path["columnsNames"]
        writer.writerow(tuple(columns))
        acu = 0
        for i in range(1,len(list_percents)+1):
            for j in range(0,list_percents[i-1]):
                acu += 1
                rows = generate_row(json_act_path,acu,i)
                for row in rows:
                    writer.writerow(row)
        f.close()
    else:
        logging.warn("Configuration arguments are wrongs")
    #except e:
        #logging.warn("Json structure")

        
if __name__ == '__main__':
    json_path = "Json_example.json"
    generate_path = "CSV_sample_exit.csv"
    number_logs = 10
    percent_per_traze = [0.25,0.75]
    main_function(json_path,generate_path,number_logs,percent_per_traze)    

