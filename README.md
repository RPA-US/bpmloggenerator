# AGOSUIRPA
Automatic generation of sintetic UI log in RPA context introducing variability

# Index


# Generate log
The software will generate a log with the characteristics defined in the screen of the second form for log generation.

(image)

The requested data are:
- **Json path:** path of the json generated with the trace.
- **Path destination log:** log generation destination path.
- **Number of logs:** number of log case to generate.
- **Percent per trace:** percentage of cases for the two possible json traces.
- **Activity decision:** activity decision node of the trace.
- **Condition:** the condition in the activity decision.
- **Variety selection:** select the random generation content of a log or use the predefined value for every node of the trace.

# Add a new function

To add a new function to the list of functions available to operate on the log, you must:
- Add the function name without parameters to the json "function_trace".
- Import the function into eltools.generic_utils.py 

# Add a new gui element to use

To add a new gui element to the list of elements available to operate on the log, you must:
- Add the element path to the json "element_trace".
