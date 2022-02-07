from lorem_text import lorem
import random
from agosuirpa.system_configuration import sep

def generate_words(args):
    '''
    Generate words. The argument is the number of words to generate.
    args:
        words: number of words to be generated. The default argument is 1 word.
    '''
    if args  == []:
        words=1
    else:
        words = args[0]
    text = lorem.words(words)
    return text


def generate_sentence(args):
    '''
    Generate one sentence.
    '''
    text =  lorem.sentence()
    return text



def generate_paragraph(args):
    '''
    Generate paragraphs. The argument is the number of paragraphs to generate.
    args:
        para: number of paragraphs to be generated
    '''
    if args  == []:
        para=1
    else:
        para = args[0]
    text =  lorem.paragraphs(para)
    return text

def generate_path(args):
    '''
    Generate path. The argument is the level of path and the extension
    args:
        value: number of levels of the path
        ext: the extension if is the path of a file 
    '''
    if args  == []:
        value=1
        ext=None
    else:
        value=args[0]
        ext=args[1] 
    res = "C:"+sep+generate_words()
    for i in range(1,value):        
        res += sep+generate_words()
    if ext is not None:
        res += ext
    return res


def generate_DNI(args):
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


def generate_random_entity(args):
    '''
    Generate a word with first letter capital 
    '''
    if args == []:
        words=1
    else:
        words = args[0]
    text = lorem.words(words).capitalize() 
    return text

def generate_clipboard_content(args):
    '''
    Generate text or paths for the paperclip content.
    '''
    res = None
    value = random.randint(1,0)
    if value == 1:
        res = generate_sentence()
    else:
        res = generate_path()
    return res