import random
import time

def generate_screenshot_demo():
    '''
    Generate a string with an extension jpg
    '''
    # Random number, the timestamp and the extension with a img identification
    return str(round(time.time() * 1000))+"_"+str(random.randint(0,1000))+"_img.jpg"