import random
import time

def generate_screenshot_demo():
    return str(round(time.time() * 1000))+"_"+str(random.randint(0,1000))+"_img.jpg"