from generator.key_generator import generate_sentence, generate_words, generate_path
import random

'''
Generate text and paths for the paperclip content. The argument is the percentage of possibilities to generate text only.
The default argument is 75 percent.
'''
def generate_paperclip_content(threshold=75):
    res = None
    value = random.randint(1,100)
    if value <= threshold:
        res = generate_sentence()
    else:
        res = generate_path()
    return res

