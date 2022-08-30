from email.policy import default
from xmlrpc.client import Boolean
from django.db import models
from django.forms import JSONField
from users.models import CustomUser
from django.contrib.postgres.fields import ArrayField

def default_phases_to_execute():
    return {'gui_components_detection': {}, 'classify_image_components': {}, 'extract_training_dataset': {}, 'decision_tree_training': {}}

# Create your models here.
class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    exp_foldername = models.CharField(max_length=255)
    exp_folder_complete_path = models.FilePathField(max_length=255)
    mode = models.CharField(max_length=255)
    scenarios_to_study = models.CharField(max_length=255, null=True)
    drop = models.CharField(max_length=255, null=True)
    special_colnames = JSONField()
    phases_to_execute = JSONField()
    decision_point_activity = models.CharField(max_length=255)
    gui_class_success_regex = models.CharField(max_length=255)
    gui_quantity_difference = models.IntegerField(default=1)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CaseStudyExecuter')
    
    def __str__(self):
        return self.title


class GUIComponentDetection(models.Model):
    eyetracking_log_filename =  models.CharField(max_length=255, default="eyetracking_log.csv")
    add_words_columns = models.BooleanField(default=False)
    overwrite_npy = models.BooleanField(default=False)

class ClassifyImageComponents(models.Model):
    model_json_file_name = models.FilePathField(max_length=255, blank=True, default="resources/models/model.json")
    model_weights = models.FilePathField(max_length=255, default="resources/models/model.h5")

class ExtractTrainingDataset(models.Model):
    columns_to_ignore = ArrayField(models.CharField(max_length=25), default=["Coor_X", "Coor_Y", "Case"])
class DecisionTreeTraining(models.Model):
    library = models.CharField(max_length=255, default='chefboost') # 'sklearn'
    algorithms = ArrayField(models.CharField(max_length=25), default=['ID3', 'CART', 'CHAID', 'C4.5'])
    mode = models.CharField(max_length=25, default='autogeneration')
    columns_to_ignore = ArrayField(models.CharField(max_length=50), default=['Timestamp_start', 'Timestamp_end'])