from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Experiment, Variations


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


class VariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variations
        fields = ('case_variation_id',
                  'case_id',
                  'scenario',
                  'activity',
                  'variant',
                  'function_name',
                  'gui_element',
                  'experiment')