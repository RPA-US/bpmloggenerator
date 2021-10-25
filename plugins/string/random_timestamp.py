import time

def generate_timestamp(args):    
    '''
    Generate a timestamp plus 1
    '''
    return str(round(time.time() * 1000)+1)
