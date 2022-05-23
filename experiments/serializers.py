from curses import beep
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Experiment, Variations

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'first_name', 'last_name']
class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        depth = 1
        fields = ['id', 'created_at', 'last_edition', 'execution_start', 'execution_finish', 'size_balance', 'name', 'description', 'number_scenarios', 
                  'variability_conf', 'scenarios_conf', 'special_colnames', 'is_being_processed', 'is_active', 'status', 'screenshots_path', 'foldername', 
                  'screenshot_name_generation_function', 'public', 'user']
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class VariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = ('case_variation_id', 'case_id', 'scenario', 'activity', 'variant', 'function_name', 'arguments', 'experiment')