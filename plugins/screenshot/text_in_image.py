import random
from lorem_text import lorem
from .replace_gui_component import insert_text_image

###################################################################################################
# Auxiliar functions
###################################################################################################

def delimit_characters(s, char_limit):
    res = "".join(s[i:i+char_limit] + "\n" for i in range(0,len(s),char_limit))
    return res

# def random_characters(case_class, max_len, max_words): #The function responsible for generating #random words which are in uppercase
#     word = '' #The variable which will hold the random word
#     size = random.randint(0, int(max_len*0.1+1))
#     size += max_len
#     if case_class == "uppercase":
#         letters = string.ascii_uppercase #A constant containing uppercase letters
#     elif case_class == "mixed":
#         letters = string.ascii_letters #A contstant containing all uppercase and lowercase letters
#     else:
#         letters = string.ascii_lowercase #A constant containing lowercase letters
#     while len(word) != size: #While loop
#         word += random.choice(letters)
#     return word
###################################################################################################


def digits_in_image(args):
    
    # Lista de dígitos
    digitos = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # Longitud del string
    n = args["digits_configuration_font"][1]
    # Inicializamos el string vacío
    res = ""
    if "digits_to_insert" in res:
        res = args["digits_to_insert"]
    else:
        # Generamos el string de n dígitos
        for i in range(n):
            res += random.choice(digitos)
    
    args["text_to_insert"] = res
    return insert_text_image(args)
    
def random_word_image(args):
    """
    Mandatory to have as args Font, Font size, Font color, Background color, Character delimitation, Random max number of word: "args": ["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF", 84, 3]
    """
    word_configuration_font = args["word_configuration_font"]
    if isinstance(word_configuration_font, list) and isinstance(word_configuration_font[0], list):
        if word_configuration_font and len(list(word_configuration_font))>2:
            if word_configuration_font[2] == "":
                size = 1
            else:
                size = random.randint(1,int(word_configuration_font[2]))
        else:
            size = 1
        s_without_linebreaks = lorem.words(size)
        if word_configuration_font[3] == '1':
            res = s_without_linebreaks[0:int(word_configuration_font[1])]
        else:
            res = delimit_characters(s_without_linebreaks,int(word_configuration_font[1]))
    else:
        size = random.randint(1,int(args["word_configuration_max_words"]))
        s_without_linebreaks = lorem.words(size)
        res = delimit_characters(s_without_linebreaks,int(args["word_configuration_chat_limit"]))
        
    args["font_configuration"] = word_configuration_font
    args["text_to_insert"] = res
    return insert_text_image(args)
    
def random_paragraph_image(args):
    """
    Mandatory to have as args Font, Font size, Font color, Background color, Character delimitation, Random max number of paragraph: "args": ["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF", 84, 3]
    [["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF"], 84, 3, newimage, capture, coordinates]
    """
    paragraph_configuration_font = args["paragraph_configuration_font"]
    
    if paragraph_configuration_font and len(list(paragraph_configuration_font))>5:
        if paragraph_configuration_font[2] == "":
            size = 1
        else:
            size = random.randint(1,int(paragraph_configuration_font[2]))
    else:
        size = random.randint(1, int(args["paragraph_configuration_max_paragraph"]))
    s = lorem.paragraphs(size)
    s_line_breaks = delimit_characters(s,int(args["paragraph_configuration_char_limit"]))
    """
        [["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF"], newimage, capture, coordinates]
    """
    args["font_configuration"] = paragraph_configuration_font
    args["text_to_insert"] = s_line_breaks
    return insert_text_image(args)
    
def random_sentence_image(args):
    """
    Mandatory to have as args Font, Font size, Font color, Background color and Character delimitation for paragraph: "args[0]":["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF", 84]
    [["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF"], 84, newimage, capture, coordinates]   
    """
    sentence_configuration_font = args["sentence_configuration_font"]
    s = lorem.sentence()
    s_line_breaks = delimit_characters(s,int(args["sentence_configuration_char_limit"]))
    """
        [["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF"], newimage, capture, coordinates]
    """
    args["font_configuration"] = sentence_configuration_font
    args["text_to_insert"] = s_line_breaks
    return insert_text_image(args)
    
def truncated_random_sentence_image(args):
    """
    Mandatory to have as args Font, Font size, Font color, Background color and Character delimitation for paragraph: "args[0]":["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF", 84]
    [["resources/Roboto-Black.ttf", 20, "#000000", "#FFFFFF"], 84, newimage, capture, coordinates]   
    """
    sentence_configuration_font = args["truncated_sentence_configuration_font"]
    trunc = int(args["truncated_sentence_configuration_char_limit"])
    i = 4
    cond = True
    while cond:
        num = int(trunc/i)
        s = lorem.words(num)
        cond = len(s) < trunc
        i-1
    s_line_breaks = s[0:num]
    args["font_configuration"] = sentence_configuration_font
    args["text_to_insert"] = s_line_breaks
    return insert_text_image(args)