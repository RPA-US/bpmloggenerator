import sys

# AGOSUIRPA API version
API_VERSION = 'api/v1/'

# AGOSUIRPA platform settings
# OS 
operating_system =sys.platform
print("Operating system detected: " + operating_system)
# Element specification filename and path separator (depends on OS)
if "linux" in operating_system:
    sep = "/"
    element_trace = "configuration"+sep+"element_trace_linux.json"
else:
    sep = "\\"
    element_trace = "configuration"+sep+"element_trace.json"
# Function specification filename
function_trace = "configuration"+sep+"function_trace.json"