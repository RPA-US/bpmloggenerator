import json
import random
import os
from agosuirpa.system_configuration import function_trace, element_trace
import secrets
import os
import zipfile
import shutil
from agosuirpa.system_configuration import sep
from experiments.models import Experiment
from users.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import serializers

# from plugins.string.random_text_lorem import generate_DNI,generate_paragraph,generate_path,generate_random_entity,generate_sentence,generate_words
# from plugins.list.coordenates_in_range import generate_mouse_position, generate_mouse_position_x,generate_mouse_position_y
# from plugins.list.mouse_tipe import generate_mousekeyboard
# from plugins.screenshot.name_screenshot import generate_screenshot_demo, generate_screenshot_without_root_path
# from plugins.screenshot.replace_gui_component import hidden_gui_element, insert_text_image, replace_gui_element_by_other, generate_copied_capture, replace_gui_element_various_places, generate_copied_capture_without_root, random_paragraph_image, random_word_image, random_sentence_image
# from plugins.app.nameapp import generate_app_demo
# from plugins.string.random_timestamp import generate_timestamp
for category in os.scandir('plugins'):
    for entry in os.scandir('plugins/'+category.name):
        if entry.is_file():
            filename = f'{entry.name}'[:-3]
            import_path = f'from plugins.{category.name}.{filename} import *'
            exec (import_path)


def detect_function(text):
    '''
    Selecting a function in the system by means of a keyword
    args:
        text: function to be detected
    '''
    # Search the function by key in the json
    f = open(function_trace)
    json_func = json.load(f)
    return eval(json_func[text])

def detect_element(text):
    '''
    Selecting an element in the system by means of a keyword
    args:
        text: element to be detected
    '''
    # Search the function by key in the json
    f = open(element_trace)
    json_func = json.load(f)
    return json_func[text]

def select_random_list(objects):
    '''
    Selecting a ramdom object of a list
    args:
        objects: elist of objects
    '''
    index = random.randint(0,len(objects)-1)      
    return objects[index]


def split_name_system(root_path):
    if "/" in root_path:
        splitted = root_path.split("/")
    if "\\" in root_path:
        splitted = root_path.split("\\")
    if "/" in root_path or "\\" in root_path:
        folder_path = sep.join(splitted)
    else:
        folder_path = root_path   
    return folder_path  

def upload_mockups(zip_path):
    zip_path = split_name_system(zip_path)
    path_without_fileextension = zip_path.split('.')[0] 
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(path_without_fileextension)
    return path_without_fileextension


@receiver(post_save, sender=CustomUser)
def create_user_experiment(sender, instance, created, **kwargs):
    if created:
        associate_experiment(user=instance)

def associate_experiment(user):

    experiments = Experiment.objects.filter(user=user.id, is_active=True)
    if experiments == None or not experiments:
        data_complete = json.load(open('resources'+sep+'template_experiments'+sep+'experiments_template.json'))
        for data in data_complete['results']:
            size_balance=data['size_balance']
            name=data['name']
            description=data['description']
            number_scenarios=int(data['number_scenarios'])
            variability_conf=data['variability_conf']
            screenshots=data['screenshots']
            special_colnames=data['special_colnames']
            screenshot_name_generation_function=data['screenshot_name_generation_function']
            foldername=data['foldername']

            experiment = Experiment(
                size_balance=size_balance,
                name=name,
                description=description,
                number_scenarios=number_scenarios,
                variability_conf=variability_conf,
                special_colnames=special_colnames,
                screenshots=screenshots,
                foldername=foldername,
                is_being_processed=False,
                is_active=True,
                user=user,
                screenshot_name_generation_function=screenshot_name_generation_function
            )
            experiment.user=user
            experiment.save()

