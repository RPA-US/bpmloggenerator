from django.db import models
from categories.models import CategoryBase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Generator(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    function_name = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        User, verbose_name="Owner", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.filename


class ExecutionResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    scenario_id = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    balance = models.CharField(max_length=255)
    generator = models.ForeignKey(Generator, on_delete=models.CASCADE)

    def __str__(self):
        return self.scenario_id+":"+self.family+"_"+self.size+"_"+self.balance

# class ExecutionConfiguration(models.Model):
#     created_at    = models.DateTimeField(auto_now_add=True)
#     scenario_id   = models.CharField(max_length=255)
#     family        = models.CharField(max_length=255)
#     size          = ArrayField(models.CharField(max_length=200))
#     balance       = ArrayField(models.CharField(max_length=200))
#     generator     = models.ForeignKey(Generator, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.scenario_id+":"+self.family+"_"+self.size+"_"+self.balance


class ExecutionConfiguration(models.Model):
    path = models.CharField(max_length=255)
    generator = models.ForeignKey(Generator, on_delete=models.CASCADE)

    def __str__(self):
        return self.path


class UILog(models.Model):
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    execution_result = models.ForeignKey(
        ExecutionResult, on_delete=models.CASCADE)

    def __str__(self):
        return self.path

# TODO: can be scaffolding


class Screenshot(models.Model):
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    execution_result = models.ForeignKey(
        ExecutionResult, on_delete=models.CASCADE)

    def __str__(self):
        return self.path


class VariabilityConfiguration(models.Model):
    path = models.CharField(max_length=255)
    is_scenario = models.BooleanField(default=False)

    def __str__(self):
        return self.path


class VariabilityTraceability(models.Model):
    case_id = models.IntegerField()
    scenario = models.CharField(max_length=10)
    case_variation_id = models.IntegerField()
    activity = models.CharField(max_length=10)
    variant = models.CharField(max_length=10)
    function_name = models.CharField(max_length=255)
    gui_element = models.CharField(max_length=255)

    def __str__(self):
        return self.gui_element


class GUIComponentCategory(CategoryBase):
    """
    The GUI components categories
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "GUI component category"
        verbose_name_plural = "GUI component categories"

    def __str__(self):
        return self.name

    # def clean(self):
    #     categ_terms = GUIComponent.objects.filter(
    #         tax_categ=self, is_tax_categ=True, active=True
    #     )
    #     if len(categ_terms) != 1:
    #         raise ValidationError(
    #             "A taxonomic category always has to have at least one associated category term"
    #         )
    #     if not (categ_terms[0].term == self.name):
    #         raise ValidationError(
    #             "A taxonomic category must always have the same name as its category term"
    #         )


class VariabilityFunctionCategory(CategoryBase):
    """
    Variability Function categories
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Variability function category"
        verbose_name_plural = "Variability function categories"

    def __str__(self):
        return self.name


class GUIComponent(models.Model):
    id_code = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField()
    gui_component_category = models.ForeignKey(
        GUIComponentCategory, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'active': True},
    )

    def __str__(self):
        return self.filename


class VariabilityFunction(models.Model):
    id_code = models.CharField(max_length=255)
    function_name = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    description = models.TextField()
    variability_function_category = models.ForeignKey(
        VariabilityFunctionCategory, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'active': True},
    )

    def __str__(self):
        return self.filename
