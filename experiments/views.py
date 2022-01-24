from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Experiment, VariabilityTraceability, VariabilityConfiguration, VariabilityFunction, VariabilityFunctionCategory, ExecutionConfiguration, ExecutionResult, GUIComponent, GUIComponentCategory, Generator
from .serializers import ExperimentSerializer, VariabilityTraceabilitySerializer, VariabilityConfigurationSerializer, VariabilityFunctionSerializer, VariabilityFunctionCategorySerializer, ExecutionConfigurationSerializer, ExecutionResultSerializer, GUIComponentSerializer, GUIComponentCategorySerializer, GeneratorSerializer
from users.models import CustomUser

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


class ExperimentView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticatedUser]
    serializer_class = ExperimentSerializer

    def get_queryset(self):
        user = self.request.user
        experiments = []
        if(user.is_anonymous is False):
            user_id = CustomUser.objects.get(user_account=self.request.user).id
            experiments = Experiment.objects.filter(user=user_id, is_active=True)
        return experiments

    def get(self, request, *args, **kwargs):
        self.serializer_class = ExperimentSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        st = status.HTTP_201_CREATED
        msg = 'ok, created'

        for data in ['launched_at', 'finished_at', 'size_balance', 'name', 'description', 'number_scenarios', 'variability_conf', 'generation_mode', 'generate_path', 'special_colnames', 'screenshot_name_generation_function']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        user_id = CustomUser.objects.get(user_account=request.user).id

        try:
            user = CustomUser.objects.get(pk=user_id)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        try:
            experiment = Experiment(
                launched_at=request.data.get('launched_at'),                  
                finished_at=request.data.get('finished_at'),                      
                size_balance=request.data.get('size_balance'),                                  
                name=request.data.get('name'),                              
                description=request.data.get('description'),                              
                number_scenarios=request.data.get('number_scenarios'),                                  
                variability_conf=request.data.get('variability_conf'),                                      
                generation_mode=request.data.get('generation_mode'),
                generate_path=request.data.get('generate_path'),                                      
                special_colnames=request.data.get('special_colnames'),                                          
                screenshot_name_generation_function=request.data.get(
                    'screenshot_name_generation_function'),
                is_active=True,
                user=user)

            experiment.save()

        except:
            msg = 'some of atributes are invalid'
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
