import random

'''
Insert one text in another text.
'''
def insert_text(text, key):
    new_text = list(text.split())
    value = random.randint(0,len(new_text)-1)
    new_text.insert(value,key)
    new_text = " ".join([str(x) for x in new_text])
    return new_text