import sys
import environ
env = environ.Env()
environ.Env.read_env()

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
if "win" in operating_system:
    sep = "\\"
    element_trace = "configuration"+sep+"element_trace.json"
else:
    sep = "/"
    element_trace = "configuration"+sep+"element_trace_linux.json"

# Function specification filename
function_trace = "configuration"+sep+"function_trace.json"



# ================================================================================
# MELRPA
# ================================================================================
decision_foldername = "decision-tree"
cropping_threshold = 2 # umbral en el solapamiento de contornos de los gui components al recortarlos
gaze_analysis_threshold = 10 # minimum time units user must spend staring at a gui component to take this gui component as a feature from the screenshot
times_calculation_mode = "seconds" # substitute "formatted" -> get times formatted "%H:%M:%S.%fS" 
metadata_location = env('METADATA_PATH')