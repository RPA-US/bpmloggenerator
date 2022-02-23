from django.db import models
from users.models import CustomUser
from private_storage.fields import PrivateFileField

class Experiment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # finished_at = models.DateTimeField(null=True, blank=True)
    size_balance = models.JSONField()#"SizeBalanceConfiguration", default=dict(default_conf)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    number_scenarios = models.IntegerField()
    variability_conf = models.JSONField()
    scenarios_conf = models.JSONField(null=True, blank=True)
    special_colnames = models.JSONField()
    screenshot_name_generation_function = models.CharField(max_length=255)
    is_being_processed=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    screenshots = PrivateFileField("Screenshots")
    screenshots_path = models.CharField(null=True, blank=True, max_length=255)
    foldername = models.CharField(null=True, blank=True, max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ExperimentOwner')
    
    def __str__(self):
        return self.foldername

class Variations(models.Model):
    case_variation_id = models.CharField(max_length=255)
    case_id = models.CharField(max_length=255)
    scenario = models.CharField(max_length=255)
    activity = models.CharField(max_length=255)
    variant = models.CharField(max_length=255)
    function_name = models.CharField(max_length=255)
    gui_element = models.CharField(max_length=255)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    def __str__(self):
        return self.case_variation_id