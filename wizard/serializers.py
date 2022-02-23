from rest_framework import serializers
from .models import GUIComponent, GUIComponentCategory, VariabilityFunction, VariabilityFunctionCategory, FunctionParam

class GUIComponentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GUIComponentCategory
        fields = ['id', 'name', 'description']


class VariabilityFunctionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VariabilityFunctionCategory
        fields = ['id', 'name', 'description']


class GUIComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GUIComponent
        fields = ['id', 'name', 'id_code', 'filename', 'path', 'description', 'gui_component_category']


class VariabilityFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariabilityFunction
        fields = ['id', 'id_code', 'function_name', 'filename', 'path', 'description', 'params', 'variability_function_category']
        
class FunctionParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionParam
        fields = ['id', 'label', 'placeholder', 'data_type', 'description', 'validation_needs']