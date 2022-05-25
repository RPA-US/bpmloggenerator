from django.contrib import admin
from .models import VariabilityFunction, VariabilityFunctionCategory, GUIComponent, GUIComponentCategory, FunctionParam, FunctionParamCategory

# Register your models here.
class GUIComponentAdmin(admin.ModelAdmin):
    exclude = ['width','height']

admin.site.register(GUIComponentCategory)
admin.site.register(GUIComponent,GUIComponentAdmin)
admin.site.register(FunctionParam)
admin.site.register(FunctionParamCategory)
admin.site.register(VariabilityFunction)
admin.site.register(VariabilityFunctionCategory)