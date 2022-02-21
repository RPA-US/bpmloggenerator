from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Experiment, VariabilityTraceability, VariabilityConfiguration, VariabilityFunction, VariabilityFunctionCategory, ExecutionConfiguration, ExecutionResult, GUIComponent, GUIComponentCategory, Generator
from .serializers import ExperimentSerializer, VariabilityTraceabilitySerializer, VariabilityConfigurationSerializer, VariabilityFunctionSerializer, VariabilityFunctionCategorySerializer, ExecutionConfigurationSerializer, ExecutionResultSerializer, GUIComponentSerializer, GUIComponentCategorySerializer, GeneratorSerializer
from users.models import CustomUser
from .functions import execute_experiment, compress_experiment
from django.http import HttpResponse
from django.http import FileResponse
# from django.core.files.storage import FileSystemStorage
import json
from agosuirpa.system_configuration import sep
from agosuirpa.generic_utils import upload_mockups
from django.shortcuts import get_object_or_404
from experiments import serializers
# class VariabilityTraceabilityViewSet(viewsets.ModelViewSet):
#     queryset = VariabilityTraceability.objects.all()
#     serializer_class = VariabilityTraceabilitySerializer


# class GeneratorViewSet(viewsets.ModelViewSet):
#     queryset = Generator.objects.all()
#     serializer_class = GeneratorSerializer


# class ExecutionResultViewSet(viewsets.ModelViewSet):
#     queryset = ExecutionResult.objects.all()
#     serializer_class = ExecutionResultSerializer


# class ExecutionConfigurationViewSet(viewsets.ModelViewSet):
#     queryset = ExecutionConfiguration.objects.all()
#     serializer_class = ExecutionConfigurationSerializer


# class VariabilityConfigurationViewSet(viewsets.ModelViewSet):
#     queryset = VariabilityConfiguration.objects.all()
#     serializer_class = VariabilityConfigurationSerializer


# class VariabilityTraceabilityViewSet(viewsets.ModelViewSet):
#     queryset = VariabilityTraceability.objects.all()
#     serializer_class = VariabilityTraceabilitySerializer


# class GUIComponentCategoryViewSet(viewsets.ModelViewSet):
#     queryset = GUIComponentCategory.objects.all()
#     serializer_class = GUIComponentCategorySerializer


# class VariabilityFunctionCategoryViewSet(viewsets.ModelViewSet):
#     queryset = VariabilityFunctionCategory.objects.all()
#     serializer_class = VariabilityFunctionCategorySerializer


# class GUIComponentViewSet(viewsets.ModelViewSet):
#     queryset = GUIComponent.objects.all()
#     serializer_class = GUIComponentSerializer


# class VariabilityFunctionViewSet(viewsets.ModelViewSet):
#     queryset = VariabilityFunction.objects.all()
#     serializer_class = VariabilityFunctionSerializer


# class VariabilityTraceabilityList(generics.ListCreateAPIView):
#     queryset = VariabilityTraceability.objects.all()
#     serializer_class = VariabilityTraceabilitySerializer

# class VariabilityTraceabilityDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = VariabilityTraceability.objects.all()
#     serializer_class = VariabilityTraceabilitySerializer

class ExperimentView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticatedUser]
    serializer_class = ExperimentSerializer

    def get_queryset(self):
        user = self.request.user
        experiments = []
        if(user.is_anonymous is False):
            user = CustomUser.objects.get(id=self.request.user.id)
            experiments = Experiment.objects.filter(user=user.id, is_active=True)
        return experiments

    def get(self, request, *args, **kwargs):
        self.serializer_class = ExperimentSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        st = status.HTTP_201_CREATED
        msg = 'ok, created'

        for data in ['size_balance', 'name', 'description', 'number_scenarios', 
                     'variability_conf', 'screenshots',
                     'special_colnames', 'screenshot_name_generation_function']:
            if not data in request.data:
                return Response({"message": "Incomplete data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=self.request.user.id)
        except:
            return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            size_balance=json.loads(request.data.get('size_balance'))
            name=request.data.get('name')
            description=request.data.get('description')
            number_scenarios=int(request.data.get('number_scenarios'))
            variability_conf=json.loads(request.data.get('variability_conf'))
            scenarios_conf=json.loads(request.data.get('scenarios_conf'))
            screenshots=request.data.get('screenshots')
            special_colnames=json.loads(request.data.get('special_colnames'))
            screenshot_name_generation_function=request.data.get('screenshot_name_generation_function')
            execute_mode=request.data.get('execute_mode')
            
            experiment = Experiment(
                size_balance=size_balance,
                name=name,
                description=description,
                number_scenarios=number_scenarios,
                variability_conf=variability_conf,
                scenarios_conf=scenarios_conf,
                special_colnames=special_colnames,
                screenshots=screenshots,
                user=user,
                screenshot_name_generation_function=screenshot_name_generation_function
            )
            experiment.save()
            
            path_without_fileextension = upload_mockups('privatefiles'+sep+experiment.screenshots.name)
            experiment.screenshots_path=path_without_fileextension
            experiment.save()
            
            if execute_mode:
                foldername = execute_experiment(experiment)
                experiment.is_being_processed=100
                experiment.is_active=True
                experiment.foldername=foldername
                experiment.save()

        except Exception as e:
            msg = 'Some of atributes are invalid: ' + str(e)
            st = status.HTTP_422_UNPROCESSABLE_ENTITY

        return Response(msg, status=st)

   
   
class ExperimentUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects.all()
    lookup_field = 'id'
    
    def put(self, request, id, *args, **kwars):
        experiment = get_object_or_404(Experiment, user=request.user, pk=id)
        st = status.HTTP_200_OK
        msg = 'Executed'

        try:
            if experiment.is_being_processed==100:
                msg = 'Experiment have been already executed'
            else:    
                foldername = execute_experiment(experiment)
                experiment.is_being_processed=100
                experiment.is_active=True
                experiment.foldername=foldername
                experiment.save()
        except Exception as e:
            msg = 'Some of atributes are invalid' + str(e)
            st = status.HTTP_422_UNPROCESSABLE_ENTITY

        return Response(msg, status=st)
        
    def delete(self, request, id, *args, **kwars):
        st = status.HTTP_200_OK
        msg = 'deleted'

        try:
            experiment = get_object_or_404(Experiment, pk=id, user=request.user.id)
            experiment.delete()
        except Exception as e:
            msg = 'Cannot delete experiment: ' + str(e)
            st = status.HTTP_409_CONFLICT

        return Response(msg, status=st)

class SmallPagesPagination(PageNumberPagination):
    page_size = 8


class ListPaginatedExperimentAPIView(generics.ListAPIView):
    """
    List active experiments
    """
    pagination_class = SmallPagesPagination
    # permission_classes = [IsAuthenticatedAdmin]
    serializer_class = ExperimentSerializer

    def get_queryset(self):
        user = self.request.user
        if(user.is_anonymous is False):
            user_id = CustomUser.objects.get(user_account=self.request.user).id
            queryset = Experiment.objects.filter(user=user_id, is_active=True)
        return queryset

class DownloadExperiment(generics.RetrieveAPIView):
    """
    Download compress experiment
    """
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if(user.is_anonymous is False):
            try:
                user = CustomUser.objects.get(id=self.request.user.id)
            except:
                return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)
            #user=user.id, dentro cuando pueda hacer experimentos 
            try:
                experiment = Experiment.objects.get(user=user.id, is_being_processed=100, id=kwargs["pk"])    
            except Exception as e:
                return Response({"message": "No experiment found: " + str(e)}, status=status.HTTP_404_NOT_FOUND)    
            
            try:        
                zip_experiment = compress_experiment(experiment)
                filename = experiment.name+".zip"
                response = FileResponse(open(zip_experiment, 'rb'))
                response['Content-Disposition'] = 'attachment; filename="%s"' % filename  
            except Exception as e:
                return Response({"message": "Experiment error: " + str(e)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return response
        else:
            return Response({"message": "No user valid"}, status=status.HTTP_401_UNAUTHORIZED)