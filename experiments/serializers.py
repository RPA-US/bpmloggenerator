from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import Experiment, Variations
from users.models import CustomUser
from users.serializers import UserExperimentSerializer

class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experiment
        fields = ['id', 'created_at', 'last_edition', 'execution_start', 'execution_finish', 'size_balance', 'name', 'description', 'number_scenarios', 
                  'variability_conf', 'scenarios_conf', 'special_colnames', 'is_being_processed', 'is_active', 'status', 'screenshots_path', 'foldername', 
                  'screenshot_name_generation_function', 'user_id']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class VariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = ('case_variation_id', 'case_id', 'scenario', 'activity', 'variant', 'function_name', 'arguments', 'experiment')