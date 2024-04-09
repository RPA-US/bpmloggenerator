import time

# def generate_timestamp(args):    
#     '''
#     Generate a timestamp plus 1
#     '''
#     return str(round(time.time() * 1000)+1)

last_timestamp = 1

def generate_timestamp():
    global last_timestamp
    new_timestamp = time.time()
    while new_timestamp <= last_timestamp:
        new_timestamp = time.time()
    last_timestamp = new_timestamp
    return new_timestamp