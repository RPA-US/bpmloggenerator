from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import CustomUser

def default_phases_to_execute():
    return ['gui_components_detection', 'classify_image_components', 'extract_training_dataset', 'decision_tree_training']

# Create your models here.
class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    exp_foldername = models.CharField(max_length=255)
    exp_folder_complete_path = models.CharField(max_length=255)
    mode = models.CharField(max_length=255)
    scenarios_to_study = models.CharField(max_length=255, null=True)
    drop = models.CharField(max_length=255, null=True)
    phases_to_execute = ArrayField(models.CharField(max_length=50), default=default_phases_to_execute)
    decision_point_activity = models.CharField(max_length=255)
    gui_class_success_regex = models.CharField(max_length=255)
    gui_quantity_difference = models.IntegerField(default=1)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='CaseStudyExecuter')
    
    def __str__(self):
        return self.title