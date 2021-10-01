import time

def generate_timestamp():    
    return str(round(time.time() * 1000)+1)
