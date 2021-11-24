# Database configuration

# Generator configuration

# operating_system = "linux"
operating_system = "windows"

if operating_system == "windows":
    sep = "\\"
    function_trace = "function_trace.json"
    element_trace = "element_trace.json"
else:
    sep = "/"
    function_trace = "function_trace.json"
    element_trace = "linux/element_trace_linux.json"

DATABASE = "resources"+sep+"databases"

# Analzer (MELRPA) case study script path
melrpa_case_study = ".." + sep + "melrpa" + sep + "melrpa" + sep + "Case_study_util.py"
autoanalize = False

# Output location
output = "CSV_exit"

# Column names
colnames = {
    "Case": "Case",
    "Activity": "Activity",
    "Screenshot": "Screenshot",
    "Variant": "Variant"
}

# Scenarios variations json location
scenarios_json = "resources"+sep+"test_scenarios"+sep+"scenarios.json"

# Default_scenario_configurations

# BASIC family
default_basic_conf = { 
    "balance":{
        "Balanced": [0.5,0.5],
        "Imbalanced": [0.4,0.6]
    },
    # Specify secuence of log sizes to automatic generation of experiments
    "size_secuence": [30,40,50,100,200],
    "families": {
        "Basic": "resources"+sep+"test_scenarios"+sep+"Basic_Act5_Var2_DesElem2.json",
    }
}

# INTERMEDIATE family
default_intermediate_conf = { 
    "balance":{
        "Balanced": [0.5,0.5],
        "Imbalanced": [0.4,0.6]
    },
    # Specify secuence of log sizes to automatic generation of experiments
    # "size_secuence": [30,40,50,100,200],
    "size_secuence": [20],
    "families": {
        "Intermediate": "resources"+sep+"test_scenarios"+sep+"Intermediate_Act8_Var2_DesElem2.json",
    }
}

# ADVANCED family
default_advanced_conf = { 
    "balance":{
        "Balanced": [0.25,0.25,0.25,0.25],
        "Imbalanced": [0.4,0.2,0.2,0.2]
    },
    # Specify secuence of log sizes to automatic generation of experiments
    "size_secuence": [30,40,50,100,200],
    "families": {
        "Advanced": "resources"+sep+"test_scenarios"+sep+"Advanced_Act10_Var2_DesElem4.json"
    }
}

default_scenario_configurations = {
    # "Basic": default_basic_conf,
    "Intermediate": default_intermediate_conf,
    # "Advanced": default_advanced_conf,
}