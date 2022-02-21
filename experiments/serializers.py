from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Experiment, VariabilityTraceability, Generator, GUIComponent, GUIComponentCategory, VariabilityConfiguration, VariabilityFunction, VariabilityFunctionCategory, ExecutionConfiguration, ExecutionResult


class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experiment
        fields = ['id', 'created_at','size_balance','name','description','number_scenarios','variability_conf','scenarios_conf','special_colnames','is_being_processed','is_active','screenshots_path','foldername','screenshot_name_generation_function']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class VariabilityTraceabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VariabilityTraceability
        fields = ('case_id',
                  'scenario',
                  'case_variation_id',
                  'activity',
                  'variant',
                  'function_name',
                  'gui_element')


class GeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generator
        fields = ['created_at', 'function_name',
                  'filename', 'path', 'description', 'owner', ]


class ExecutionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionResult
        fields = ['scenario_id', 'family', 'size', 'balance', 'generator']


class ExecutionConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionConfiguration
        fields = ['path', 'generator']


class VariabilityConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariabilityConfiguration
        fields = ['path', 'is_scenario']


class VariabilityTraceabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VariabilityTraceability
        fields = ['case_id', 'scenario', 'case_variation_id',
                  'activity', 'variant', 'function_name', 'gui_element']


class GUIComponentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GUIComponentCategory
        fields = ['name']


class VariabilityFunctionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VariabilityFunctionCategory
        fields = ['name']


class GUIComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GUIComponent
        fields = ['id_code', 'filename', 'path',
                  'description', 'gui_component_category']


class VariabilityFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariabilityFunction
        fields = ['id_code', 'filename', 'path',
                  'description', 'variability_function_category']
