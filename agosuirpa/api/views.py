from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import VariabilityTraceability, VariabilityConfiguration, VariabilityFunction, VariabilityFunctionCategory, ExecutionConfiguration, ExecutionResult, GUIComponent, GUIComponentCategory, Generator
from .serializers import VariabilityTraceabilitySerializer, VariabilityConfigurationSerializer, VariabilityFunctionSerializer, VariabilityFunctionCategorySerializer, ExecutionConfigurationSerializer, ExecutionResultSerializer, GUIComponentSerializer, GUIComponentCategorySerializer, GeneratorSerializer
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class VariabilityTraceabilityViewSet(viewsets.ModelViewSet):
    queryset = VariabilityTraceability.objects.all()
    serializer_class = VariabilityTraceabilitySerializer


class GeneratorViewSet(viewsets.ModelViewSet):
    queryset = Generator.objects.all()
    serializer_class = GeneratorSerializer


class ExecutionResultViewSet(viewsets.ModelViewSet):
    queryset = ExecutionResult.objects.all()
    serializer_class = ExecutionResultSerializer


class ExecutionConfigurationViewSet(viewsets.ModelViewSet):
    queryset = ExecutionConfiguration.objects.all()
    serializer_class = ExecutionConfigurationSerializer


class VariabilityConfigurationViewSet(viewsets.ModelViewSet):
    queryset = VariabilityConfiguration.objects.all()
    serializer_class = VariabilityConfigurationSerializer


class VariabilityTraceabilityViewSet(viewsets.ModelViewSet):
    queryset = VariabilityTraceability.objects.all()
    serializer_class = VariabilityTraceabilitySerializer


class GUIComponentCategoryViewSet(viewsets.ModelViewSet):
    queryset = GUIComponentCategory.objects.all()
    serializer_class = GUIComponentCategorySerializer


class VariabilityFunctionCategoryViewSet(viewsets.ModelViewSet):
    queryset = VariabilityFunctionCategory.objects.all()
    serializer_class = VariabilityFunctionCategorySerializer


class GUIComponentViewSet(viewsets.ModelViewSet):
    queryset = GUIComponent.objects.all()
    serializer_class = GUIComponentSerializer


class VariabilityFunctionViewSet(viewsets.ModelViewSet):
    queryset = VariabilityFunction.objects.all()
    serializer_class = VariabilityFunctionSerializer


# class VariabilityTraceabilityList(generics.ListCreateAPIView):
#     queryset = VariabilityTraceability.objects.all()
#     serializer_class = VariabilityTraceabilitySerializer

# class VariabilityTraceabilityDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = VariabilityTraceability.objects.all()
#     serializer_class = VariabilityTraceabilitySerializer


# api/urls.py
# from rest_framework.urlpatterns import format_suffix_patterns
# from api import views
# urlpatterns = [
#     path('', views.VariabilityTraceabilityList.as_view()),
#     path('<int:pk>/', views.VariabilityTraceabilityDetail.as_view()),
# ]
