from django.shortcuts import render
from rest_framework import generics, status, viewsets
from .models import VariabilityFunction, VariabilityFunctionCategory, GUIComponent, GUIComponentCategory, FunctionParam
from .serializers import VariabilityFunctionSerializer, VariabilityFunctionCategorySerializer, GUIComponentSerializer, GUIComponentCategorySerializer, FunctionParamSerializer

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

class FunctionParamViewSet(viewsets.ModelViewSet):
    queryset = FunctionParam.objects.all()
    serializer_class = FunctionParamSerializer

# class GUIComponentView(generics.ListCreateAPIView):
#     # permission_classes = [IsAuthenticatedUser]
#     serializer_class = ExperimentSerializer

#     def get_queryset(self):
#         user = self.request.user
#         experiments = []
#         if(user.is_anonymous is False):
#             user = CustomUser.objects.get(id=self.request.user.id)
#             experiments = Experiment.objects.filter(user=user.id, is_active=True)
#         return experiments

#     def get(self, request, *args, **kwargs):
#         self.serializer_class = ExperimentSerializer
#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         st = status.HTTP_201_CREATED
#         msg = 'ok, created'

#         # TODO: serializer
        
#         try:
#             user = CustomUser.objects.get(id=self.request.user.id)
#         except:
#             return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)

#         try:
#            # TODO: save

#         except Exception as e:
#             msg = 'Some of atributes are invalid: ' + str(e)
#             st = status.HTTP_422_UNPROCESSABLE_ENTITY

#         return Response({"message": msg, "id": experiment.id}, status=st)