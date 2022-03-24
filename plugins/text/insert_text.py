import random

def insert_text(text, key):
    '''
    Insert one text in another text.
    args:
        text: destination text
        key: word to insert
    '''
    # Is randomized among the existing words of a text without breaking up words 
    new_text = list(str(text).split())
    value = random.randint(0,len(new_text)-1)
    new_text.insert(value,str(key))
    new_text = " ".join([str(x) for x in new_text])
    return new_text