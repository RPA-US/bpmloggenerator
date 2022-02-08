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
from agosuirpa.system_configuration import generate_path, sep
from agosuirpa.generic_utils import upload_mockups
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

        for data in ['size_balance', 'name', 'description', 'number_scenarios', 'variability_conf', 'generation_mode', 'screenshots', 'special_colnames', 'screenshot_name_generation_function']:
            if not data in request.data:
                return Response({"message": "Incomplete data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=self.request.user.id)
        except:
            return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            size_balance=json.loads(request.data.get('size_balance'))
            number_scenarios=request.data.get('number_scenarios')
            name=request.data.get('name')
            description=request.data.get('description')
            number_scenarios=int(request.data.get('number_scenarios'))
            variability_conf=json.loads(request.data.get('variability_conf'))
            scenarios_conf=json.loads(request.data.get('scenarios_conf'))
            generation_mode=request.data.get('generation_mode')
            screenshots=request.data.get('screenshots')
            special_colnames=json.loads(request.data.get('special_colnames'))
            screenshot_name_generation_function=request.data.get('screenshot_name_generation_function')
            
            # fs = FileSystemStorage()
            # name = fs.save(uploaded_file.name, uploaded_file)

            
            experiment = Experiment(
                size_balance=size_balance,
                name=name,
                description=description,
                number_scenarios=number_scenarios,
                variability_conf=variability_conf,
                generation_mode=generation_mode,
                special_colnames=special_colnames,
                screenshots=screenshots,
                is_being_processed=True,
                is_active=False,
                user=user,
                screenshot_name_generation_function=screenshot_name_generation_function
            )
            
            
            experiment.save()
            path_without_fileextension = upload_mockups('privatefiles'+sep+experiment.screenshots.name)
            foldername = execute_experiment(experiment,
                                generation_mode,
                                number_scenarios,
                                variability_conf,
                                size_balance,
                                scenarios_conf,
                                generate_path,
                                special_colnames,
                                path_without_fileextension,
                                screenshot_name_generation_function)
            
            
            experiment.is_being_processed=False
            experiment.is_active=True
            experiment.foldername=foldername
            experiment.save()
            

        except Exception as e:
            msg = 'Some of atributes are invalid: ' + str(e)
            st = status.HTTP_422_UNPROCESSABLE_ENTITY

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
                experiment = Experiment.objects.get(user=user.id,id=kwargs["pk"])    
            except:
                return Response({"message": "No experiment found"}, status=status.HTTP_404_NOT_FOUND)    
            try:        
                zip_experiment = compress_experiment(experiment)
                filename = experiment.name+".zip"
                response = FileResponse(open(zip_experiment, 'rb'))
                response['Content-Disposition'] = 'attachment; filename="%s"' % filename  
            except:
                return Response({"message": "Experiment error try another"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return response
        else:
            return Response({"message": "No user valid"}, status=status.HTTP_401_UNAUTHORIZED)