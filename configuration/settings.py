# OS configuration 

# operating_system = "linux"
operating_system = "windows"

function_trace = "function_trace.json"
if operating_system == "windows":
    sep = "\\"
    element_trace = "element_trace.json"
else:
    sep = "/"
    element_trace = "configuration_linux/element_trace_linux.json"

###########################
# Generator configuration #
###########################
output = "CSV_exit" # Output location

scenarios_json = "resources"+sep+"scenarios_json"+sep+"scenarios.json"# Scenarios variations json location
scenario_size = 30
decision_activity = "D"
# Column names
colnames = {
    "Case": "Case",
    "Activity": "Activity",
    "Screenshot": "Screenshot",
    "Variant": "Variant"
}


# Default_scenario_configurations
# BASIC family
default_basic_conf = { 
    "balance":{
        "Balanced": [0.5,0.5],
        "Imbalanced": [0.25,0.75]
    },
    # Specify secuence of log sizes to automatic generation of experiments
    "size_secuence": [10,25],#50,100],
    "families": {
        "Basic": "resources"+sep+"scenarios_json"+sep+"Basic_Act5_Var2_DesElem2.json",
    }
}

# INTERMEDIATE family
default_intermediate_conf = { 
    "balance":{
        "Balanced": [0.5,0.5],
        "Imbalanced": [0.25,0.75]
    },
    # Specify secuence of log sizes to automatic generation of experiments
    # "size_secuence": [25,50,100],
    "size_secuence": [10,25,50,100],
    "families": {
        "Intermediate": "resources"+sep+"scenarios_json"+sep+"Intermediate_Act8_Var2_DesElem2.json",
    }
}

# ADVANCED family
default_advanced_conf = { 
    "balance":{
        "Balanced": [0.25,0.25,0.25,0.25],
        "Imbalanced": [0.4,0.2,0.2,0.2]
    },
    # Specify secuence of log sizes to automatic generation of experiments
    "size_secuence": [10,25,50,100],
    "families": {
        "Advanced": "resources"+sep+"scenarios_json"+sep+"Advanced_Act10_Var2_DesElem4.json"
    }
}

default_scenario_configurations = {
    "Basic": default_basic_conf,
    # "Intermediate": default_intermediate_conf,
    # "Advanced": default_advanced_conf,
}

##########################
# Database configuration #
##########################
DATABASE = "resources"+sep+"databases"

##########################
# Analzer (MELRPA) 
##########################
melrpa_case_study = ".." + sep + "melrpa" + sep + "melrpa" + sep + "Case_study_util.py" # case study script path
autoanalize = False