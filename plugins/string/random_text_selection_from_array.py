from generator.key_generator import generate_sentence, generate_words, generate_path
import random


def generate_clipboard_content():
    '''
    Generate text or paths for the paperclip content.
    '''
    res = None
    value = random.randint(1,0)
    if value ==1:
        res = generate_sentence()
    else:
        res = generate_path()
    return res
