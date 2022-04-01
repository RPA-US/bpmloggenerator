def generate_screenshot_demo(args):
    '''
    Generate an image name as string with an extension png
    '''
    # Random number and the extension with a img identification
    generate_path = str(args[0])
    number = int(args[1])
    return generate_path+str(number)+"_img.png"

def generate_screenshot_without_root_path(args):
    '''
    Generate an image name without root path as string with an extension png
    '''
    # Random number and the extension with a img identification
    generate_path = str(args[0])
    number = int(args[1])
    return str(number)+"_img.png"