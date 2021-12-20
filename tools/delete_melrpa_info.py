import os
import shutil

def get_only_list_folders(path, sep):
    folders_and_files = os.listdir(path)
    family_names = []
    for f in folders_and_files:
        if os.path.isdir(path+sep+f):
            family_names.append(f)
    return family_names

path = os.getcwd() # "CSV_exit\\resources"
print("Deleting files in... " + path)
sep = "\\"

folders_to_remove = ["components_npy", "contornos"]
files_to_remove = ["preprocessed_dataset.csv", "decision_tree.log", "enriched_log.csv", "images_ocr_info.txt"]

scenarios = get_only_list_folders(path,sep)

for scenario in scenarios:
    for f in get_only_list_folders(path+sep+scenario, sep):  
        for file in files_to_remove:
            if os.path.exists(path+sep+scenario+sep+f+sep+file):
                os.remove(path+sep+scenario+sep+f+sep+file)
            else:
                print("The file does not exist")
        for folder in folders_to_remove:
            if os.path.isdir(path+sep+scenario+sep+f+sep+folder):
                shutil.rmtree(path+sep+scenario+sep+f+sep+folder)
            else:
                print("The folder does not exist or isn't a folder")