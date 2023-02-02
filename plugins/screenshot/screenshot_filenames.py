import shutil

def generate_copied_capture(args):
    '''
    Generate an image copy renamed
    '''
    capture = args["original_image_path"]
    generate_path  = args["image_path_to_save"]
    number = args["to_concatenate"]    
    
    if not '.png' in str(number):
        name = generate_path+str(number)+"_img.png"
    else:
        name = generate_path+str(number)
    shutil.copyfile(capture, name)
    # Random number and the extension with a img identification
    return name

def generate_copied_capture_without_root(args):
    '''
    Generate an image copy renamed
    '''
    capture = args["original_image_path"]
    generate_path  = args["image_path_to_save"]
    number = args["number_to_concatenate"]
    
    name = str(number)+"_img.png"
    shutil.copyfile(capture, generate_path+name)
    # Random number and the extension with a img identification
    return name