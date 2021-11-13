# Database configuration

# Generator configuration

DATABASE = "loggenerator.db"

operating_system = "linux" #"windows"

if operating_system == "windows":
    sep = "\\"
    function_trace = "function_trace.json"
    element_trace = "element_trace.json"
else:
    sep = "/"
    function_trace = "linux/function_trace_linux.json"
    element_trace = "linux/element_trace_linux.json"