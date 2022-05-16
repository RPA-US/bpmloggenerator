from email.mime import image
from enum import unique
from django.db import models
from categories.models import CategoryBase
from private_storage.fields import PrivateImageField
# from django_postgres_extensions.models.fields import ArrayField

class GUIComponentCategory(CategoryBase):
    """
    The GUI components categories
    """

    name = models.CharField(max_length=75, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "GUI component category"
        verbose_name_plural = "GUI component categories"

    def __str__(self):
        return self.name

class GUIComponent(models.Model):
    id_code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    width = models.PositiveSmallIntegerField(default=0)
    height = models.PositiveSmallIntegerField(default=0)
    image = PrivateImageField("Image", width_field='width', height_field='height')
    gui_component_category = models.ForeignKey(
        GUIComponentCategory, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'active': True},
    )
    
    def __str__(self):
        return self.filename

class VariabilityFunctionCategory(CategoryBase):
    """
    Variability Function categories
    """
    name = models.CharField(max_length=75, unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Variability function category"
        verbose_name_plural = "Variability function categories"

    def __str__(self):
        return self.name

class FunctionParamCategory(models.Model):
    label = models.CharField(max_length=75, unique=True)
    placeholder = models.CharField(max_length=75)
    data_type = models.CharField(max_length=75)
    description = models.CharField(max_length=255)
    validation_needs = models.JSONField() # TODO
    
    def __str__(self):
        return self.label     

class VariabilityFunction(models.Model):
    id_code = models.CharField(max_length=255, unique=True)
    function_name = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField()
    variability_function_category = models.ForeignKey(VariabilityFunctionCategory, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'active': True},)
        
    def __str__(self):
        return self.filename

class FunctionParam(models.Model):
    id_code = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(blank=False)
    description = models.CharField(max_length=255)
    function_param_category = models.ForeignKey(FunctionParamCategory, blank=False, null=False, on_delete=models.CASCADE)
    validation_needs = models.JSONField() # TODO
    variability_function = models.ForeignKey(VariabilityFunction,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_code 
