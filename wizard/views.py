from rest_framework import viewsets
from rest_framework.response import Response
from .models import VariabilityFunction, VariabilityFunctionCategory, GUIComponent, GUIComponentCategory, FunctionParam
from .serializers import VariabilityFunctionSerializer, VariabilityFunctionCategorySerializer, GUIComponentSerializer, GUIComponentCategorySerializer, FunctionParamSerializer

class GUIComponentCategoryViewSet(viewsets.ModelViewSet):
    queryset = GUIComponentCategory.objects.all()
    serializer_class = GUIComponentCategorySerializer
    
    def list(self, request):
        serializer = GUIComponentCategorySerializer(self.queryset, many=True)
        return Response({"results": serializer.data})

class VariabilityFunctionCategoryViewSet(viewsets.ModelViewSet):
    queryset = VariabilityFunctionCategory.objects.all()
    serializer_class = VariabilityFunctionCategorySerializer
    
    def list(self, request):
        serializer = VariabilityFunctionCategorySerializer(self.queryset, many=True)
        return Response({"results": serializer.data})

class GUIComponentViewSet(viewsets.ModelViewSet):
    queryset = GUIComponent.objects.all()
    serializer_class = GUIComponentSerializer

    def list(self, request):
        serializer = GUIComponentSerializer(self.queryset, many=True)
        return Response({"results": serializer.data})
class VariabilityFunctionViewSet(viewsets.ModelViewSet):
    queryset = VariabilityFunction.objects.all()
    serializer_class = VariabilityFunctionSerializer

    def list(self, request):
        serializer = VariabilityFunctionSerializer(self.queryset, many=True)
        return Response({"results": serializer.data})
    
class FunctionParamViewSet(viewsets.ModelViewSet):
    queryset = FunctionParam.objects.all()
    serializer_class = FunctionParamSerializer
    
    def list(self, request):
        serializer = FunctionParamSerializer(self.queryset, many=True)
        return Response({"results": serializer.data})