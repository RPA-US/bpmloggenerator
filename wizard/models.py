from email.mime import image
from enum import unique
from django.db import models
from categories.models import CategoryBase
from django.core.exceptions import ValidationError
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
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
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

class FunctionParam(models.Model):
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
    params = models.ManyToManyField(FunctionParam, through='ParamAssign',blank=True)
    variability_function_category = models.ForeignKey(
        VariabilityFunctionCategory, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'active': True},
    )
        
    def __str__(self):
        return self.filename

class ParamAssign(models.Model):
    #id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    order = models.IntegerField(blank=False)
    variabilityFunction = models.ForeignKey(VariabilityFunction, on_delete=models.CASCADE)
    functionParam = models.ForeignKey(FunctionParam, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("id","functionParam", "order"),)