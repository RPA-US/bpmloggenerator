from lorem_text import lorem
import random

def generate_words(words=1):
    '''
    Generate words. The argument is the number of words to generate.
    args:
        words: number of words to be generated. The default argument is 1 word.
    '''
    text = lorem.words(words)
    return text


def generate_sentence():
    '''
    Generate one sentence.
    '''
    text =  lorem.sentence()
    return text



def generate_paragraph(para=1):
    '''
    Generate paragraphs. The argument is the number of paragraphs to generate.
    args:
        para: number of paragraphs to be generated
    '''
    text =  lorem.paragraphs(para)
    return text

def generate_path(value=1,ext=None):
    '''
    Generate path. The argument is the level of path and the extension
    args:
        value: number of levels of the path
        ext: the extension if is the path of a file 
    '''
    res = "C:\\"+generate_words()
    for i in range(1,value):        
        res += "\\"+generate_words()
    if ext is not None:
        res += ext
    return res


def generate_DNI():
    '''
    Generate spanish number identification.
    '''
    DNI = 0
    value = random.randint(1,99999999)
    number_control = value%23
    value = str(value)
    letters = {0:"T",1:"R",2:"W",3:"A",4:"G",5:"M",6:"Y",7:"F",8:"P",9:"D",10:"X", 11:"B",12:"N",13:"J",14:"Z",15:"S",16:"Q",17:"V",18:"H",19:"L",20:"C",21:"K",22:"E"}
    for i in range(0,(8-len(value))): value="0"+value
    DNI = str(value)+letters[number_control]
    return DNI


def generate_random_entity():
    '''
    Generate a word with first letter capital 
    '''
    text = lorem.words(words).capitalize() 
    return text



