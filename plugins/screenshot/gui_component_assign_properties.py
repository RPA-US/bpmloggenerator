
def gui_component_status(args):
    """
    This function takes as argument an UI element status and set it as its property in the json properties
    """
    status = args[0][0]
    process_info = args[len(args)-1]
    process_info["object_json_properties"]["status"] = status
    
    return status, process_info["object_json_properties"]
    