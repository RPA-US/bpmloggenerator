import sys
import environ
env = environ.Env()
environ.Env.read_env()

# MELRPA CUSTOM CONFIGURATIONS
operating_system = sys.platform

if "win" in operating_system:
    sep = "\\"
    element_trace = "configuration"+sep+"element_trace.json"
else:
    sep = "/"
    element_trace = "configuration"+sep+"element_trace_linux.json"

decision_foldername = "decision-tree"
cropping_threshold = 2 # umbral en el solapamiento de contornos de los gui components al recortarlos
gaze_analysis_threshold = 10 # minimum time units user must spend staring at a gui component to take this gui component as a feature from the screenshot
times_calculation_mode = "seconds" # substitute "formatted" -> get times formatted "%H:%M:%S.%fS" 
metadata_location = env('METADATA_PATH')