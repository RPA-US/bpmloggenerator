from lorem_text import lorem
import random
'''
Generate words. The argument is the number of words to generate.
The default argument is 1 word.
'''
def generate_words(words=1):
    text = lorem.words(words)
    return text


'''
Generate one sentence.
'''
def generate_sentence():
    text =  lorem.sentence()
    return text


'''
Generate paragraphs. The argument is the number of paragraphs to generate.
The default argument is 1 paragraph.
'''
def generate_paragraph(para=1):
    text =  lorem.paragraphs(para)
    return text


'''
generar ruta
'''
def generate_path():
    res = "C:\\"+generate_words()+"\\"+generate_words()+"\\"+generate_words()
    return res

'''
Generate spanish number identification.
'''
def generate_DNI():
    DNI = 0
    value = random.randint(1,99999999)
    number_control = value%23
    value = str(value)
    letters = {0:"T",1:"R",2:"W",3:"A",4:"G",5:"M",6:"Y",7:"F",8:"P",9:"D",10:"X", 11:"B",12:"N",13:"J",14:"Z",15:"S",16:"Q",17:"V",18:"H",19:"L",20:"C",21:"K",22:"E"}
    for i in range(0,(8-len(value))): value="0"+value
    DNI = str(value)+letters[number_control]
    return DNI


'''
Generate entity.
'''
def generate_random_entity(words=1):
    text = lorem.words(words).capitalize() 
    return text


'''
Insert one text in another text.
'''
def insert_text(text, key):
    new_text = list(text.split())
    value = random.randint(0,len(new_text)-1)
    new_text.insert(value,key)
    new_text = " ".join([str(x) for x in new_text])
    return new_text
