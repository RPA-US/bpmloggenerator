from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'last_login', 'date_joined', 'is_staff')

class UserExperimentSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'first_name', 'last_name')