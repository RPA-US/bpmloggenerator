import sys

# AGOSUIRPA API version
API_VERSION = 'api/v1/'

prefix_scenario = "sc_"
experiment_results_path = "CSV_exit"
ui_logs_foldername = "UI_logs"
additional_scenarios_resources_foldername = "additional_scenarios_resources"

# AGOSUIRPA platform settings
# OS 
operating_system =sys.platform
print("Operating system detected: " + operating_system)
# Element specification filename and path separator (depends on OS)
if "windows" in operating_system:
    sep = "\\"
    element_trace = "configuration"+sep+"element_trace.json"
else:
    sep = "/"
    element_trace = "configuration"+sep+"element_trace_linux.json"
# Function specification filename
function_trace = "configuration"+sep+"function_trace.json"