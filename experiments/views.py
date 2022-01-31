from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Experiment, VariabilityTraceability, VariabilityConfiguration, VariabilityFunction, VariabilityFunctionCategory, ExecutionConfiguration, ExecutionResult, GUIComponent, GUIComponentCategory, Generator
from .serializers import ExperimentSerializer, VariabilityTraceabilitySerializer, VariabilityConfigurationSerializer, VariabilityFunctionSerializer, VariabilityFunctionCategorySerializer, ExecutionConfigurationSerializer, ExecutionResultSerializer, GUIComponentSerializer, GUIComponentCategorySerializer, GeneratorSerializer
from users.models import CustomUser
from .functions import execute_experiment

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

        for data in ['size_balance', 'name', 'description', 'number_scenarios', 'variability_conf', 'generation_mode', 'generate_path', 'special_colnames', 'screenshot_name_generation_function']:
            if not data in request.data:
                return Response({"message": "Incomplete data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=self.request.user.id)
        except:
            return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            # finished_at=request.data.get('finished_at')                   
            size_balance=request.data.get('size_balance')
            number_scenarios=request.data.get('number_scenarios')
            name=request.data.get('name')                              
            description=request.data.get('description')                              
            number_scenarios=request.data.get('number_scenarios')                                  
            variability_conf=request.data.get('variability_conf')  
            scenarios_conf=request.data.get('scenarios_conf')                                                                          
            generation_mode=request.data.get('generation_mode')
            generate_path=request.data.get('generate_path')                                      
            special_colnames=request.data.get('special_colnames')                                          
            screenshot_name_generation_function=request.data.get(
                'screenshot_name_generation_function')
            
            experiment = Experiment(
                size_balance=size_balance,
                name=name,
                description=description,
                number_scenarios=number_scenarios,
                variability_conf=variability_conf,
                generation_mode=generation_mode,
                generate_path=generate_path,
                special_colnames=special_colnames,
                is_being_processed=True,
                is_active=False,
                user=user,
                screenshot_name_generation_function=screenshot_name_generation_function
            )
            experiment.save()

            foldername = execute_experiment(experiment,
                                generation_mode,
                                number_scenarios,
                                variability_conf,
                                size_balance,
                                scenarios_conf,
                                generate_path,
                                special_colnames,
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
        if(user.is_anonymous is False and user.authority == 'BAR'):
            user_id = CustomUser.objects.get(user_account=self.request.user).id
            queryset = Experiment.objects.filter(user=user_id, is_active=True)
        return queryset
