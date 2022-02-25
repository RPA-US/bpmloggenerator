from email.mime import image
from django.db import models
from categories.models import CategoryBase
from django.core.exceptions import ValidationError
# from django_postgres_extensions.models.fields import ArrayField

class GUIComponentCategory(CategoryBase):
    """
    The GUI components categories
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "GUI component category"
        verbose_name_plural = "GUI component categories"

    def __str__(self):
        return self.name

class GUIComponent(models.Model):
    name = models.CharField(max_length=255)
    id_code = models.CharField(max_length=255)
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
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Variability function category"
        verbose_name_plural = "Variability function categories"

    def __str__(self):
        return self.name

class FunctionParam(models.Model):
    label = models.CharField(max_length=50)
    placeholder = models.CharField(max_length=50)
    data_type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    validation_needs = models.JSONField() # TODO
    
    def __str__(self):
        return self.label    
    
class VariabilityFunction(models.Model):
    id_code = models.CharField(max_length=255)
    function_name = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField()
    params = models.ManyToManyField(FunctionParam)
    variability_function_category = models.ForeignKey(
        VariabilityFunctionCategory, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'active': True},
    )
        
    def __str__(self):
        return self.filename
    
    
    # GUI Variation
    #     image
    #     coordenates
    #     variability_function
    #     gui_type
    #     experiment