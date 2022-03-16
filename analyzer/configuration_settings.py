import sys
import environ
env = environ.Env()
environ.Env.read_env()

# MELRPA CUSTOM CONFIGURATIONS
operating_system =sys.platform

if "win" in operating_system:
    sep = "\\"
    element_trace = "configuration"+sep+"element_trace.json"
else:
    sep = "/"
    element_trace = "configuration"+sep+"element_trace_linux.json"

threshold = 2
times_calculation_mode = "seconds" # substitute "formatted" -> get times formatted "%H:%M:%S.%fS" 
metadata_location = env('METADATA_PATH')