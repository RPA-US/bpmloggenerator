from rest_framework.serializers import ModelSerializer
from .models import CustomUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'last_login', 'date_joined', 'is_staff')

class UserExperimentSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('url', 'username', 'email', 'groups', 'first_name', 'last_name')