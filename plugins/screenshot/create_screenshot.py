import os
import tools.generic_utils as util

def generate_screenshot_demo(args):
    '''
    Generate an image name as string with an extension png
    '''
    # Random number and the extension with a img identification
    generate_path = args[0]
    number = args[1]
    return generate_path+str(number)+"_img.png"


def change_screenshot_name(args):
    '''
    Generate an image copy renamed
    '''
    capture = args[0]
    generate_path = args[1]
    number = args[2]
    name = generate_screenshot_demo([generate_path,number])
    shutil.copyfile(capture, name)
    # Random number and the extension with a img identification
    return name


def generate_capture(columns_ui,columns,element,acu,generate_path,attr):
    '''
    Generate row reading the json
    args:
        dict: json with the trace
        acu: number of the case
        variante: if use the initial value or the generate
    '''    
    pathA = os.getcwd()
    capturePath= element["initValue"]
    args_tmp = element["args"]
    args = [generate_path,acu]
    new_image = generate_screenshot_demo(args)
    try:
        for i in columns_ui:
            try:
                arguments = []
                if i in columns:
                    ind_text = columns.index(i)
                    content = attr[ind_text]
                    arguments.append(content)
                if i in args_tmp:
                    func = args_tmp[i]
                    for j in func:
                        if element is not None:
                            coordinates = j["coordinates"]
                            name = j["name"]
                            args = j["args"]
                            if os.path.exists(pathA+"\\"+new_image):
                                capturePath=new_image
                            arguments.append(args)
                            arguments.append(new_image)
                            arguments.append(capturePath)
                            arguments.append(coordinates)
                            new_image = util.detect_function(name)(arguments)
                        else:
                            new_image="NaN"
                        arguments = []
            except:
                arguments = []
    except:
        new_image = "NaN"
    return new_image