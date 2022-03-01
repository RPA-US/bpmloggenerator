from django.db import models
from users.models import CustomUser
from private_storage.fields import PrivateFileField
from django.core.exceptions import ValidationError
from enum import Enum


class ExperimentStatusChoice(Enum):   # A subclass of Enum
    PR = "PRE_SAVED"
    SA = "SAVED"
    LA = "LAUNCHED"
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Experiment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    # Nullable attributes
    last_edition = models.DateTimeField(null=True, blank=True)
    execution_start = models.DateTimeField(null=True, blank=True)
    execution_finish = models.DateTimeField(null=True, blank=True)
    size_balance = models.JSONField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    number_scenarios = models.IntegerField(null=True, blank=True)
    variability_conf = models.JSONField(null=True, blank=True)
    scenarios_conf = models.JSONField(null=True, blank=True)
    special_colnames = models.JSONField(null=True, blank=True)
    screenshots = PrivateFileField("Screenshots", null=True)
    screenshots_path = models.CharField(null=True, blank=True, max_length=255)
    foldername = models.CharField(null=True, blank=True, max_length=255)
    # Internal configuration attributes
    status = models.CharField(max_length=255, choices=ExperimentStatusChoice.choices())
    screenshot_name_generation_function = models.CharField(max_length=255)
    is_being_processed=models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ExperimentOwner')
    
    def __str__(self):
        return self.name
        
    def clean(self):
        if self.status == ExperimentStatusChoice.PR.value:
            if not hasattr(self, 'screenshots'):
                raise ValidationError(
                    "To use wizard, experiment must contains its associated screenshots"
                )

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