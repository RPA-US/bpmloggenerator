from generator.key_generator import generate_paragraph, generate_sentence, generate_words, generate_DNI, insert_text,generate_random_entity
from generator.paperclip_generator import generate_paperclip_content
from generator.screenResolution_generator import image_resolution
from generator.mouse_generator import generate_mouse_position

if __name__ == '__main__':
    position = (1900,1079)
    resolution = (1920,1080)
    height = 50
    width = 75
    print(generate_mouse_position(position, resolution,height ,width))

