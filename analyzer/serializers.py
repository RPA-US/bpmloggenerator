from rest_framework import serializers
from .models import CaseStudy

class CaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__' # ['id', 'title', 'created_at', 'mode', 'exp_version_name', 'phases_to_execute', 'decision_point_activity', 'path_to_save_experiment', 'gui_class_success_regex', 'gui_quantity_difference', 'scenarios_to_study', 'drop', 'user']