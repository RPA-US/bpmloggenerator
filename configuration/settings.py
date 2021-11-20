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