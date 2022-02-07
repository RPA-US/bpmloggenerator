import secrets
import os
import zipfile
import shutil
from agosuirpa.system_configuration import sep

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

def generate_path():
    urlsafe = secrets.token_urlsafe(32)
    media_path = split_name_system(STATIC_ROOT)  
    media_path = media_path+sep+urlsafe     
    if not os.path.media_path(media_path):
        os.mkdir(media_path)
    else:
        generate_path(user)
    return media_path

def upload_mockups(zip_path):
    print(zip_path)
    zip_path = split_name_system(zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(zip_path.split('.')[0])
    return zip_path
