from rest_framework import viewsets
from rest_framework.response import Response
from users.permissions import IsActive
from .models import VariabilityFunction, VariabilityFunctionCategory, GUIComponent, GUIComponentCategory, FunctionParam, ParamAssign
from .serializers import VariabilityFunctionSerializer, VariabilityFunctionCategorySerializer, GUIComponentSerializer, GUIComponentCategorySerializer, FunctionParamSerializer, ParamAssignSerializer

class GUIComponentCategoryViewSet(viewsets.ModelViewSet):
    queryset = GUIComponentCategory.objects.all()
    serializer_class = GUIComponentCategorySerializer
    permission_classes = [IsActive]
    
    def list(self, request):
        serializer = GUIComponentCategorySerializer(self.queryset, many=True)
        return Response({"results": serializer.data})

class VariabilityFunctionCategoryViewSet(viewsets.ModelViewSet):
    queryset = VariabilityFunctionCategory.objects.all()
    serializer_class = VariabilityFunctionCategorySerializer
    permission_classes = [IsActive]
    
    def list(self, request):
        serializer = VariabilityFunctionCategorySerializer(self.queryset, many=True)
        return Response({"results": serializer.data})

class GUIComponentViewSet(viewsets.ModelViewSet):
    queryset = GUIComponent.objects.all()
    serializer_class = GUIComponentSerializer
    permission_classes = [IsActive]

    def list(self, request):
        serializer = GUIComponentSerializer(self.queryset, many=True)
        return Response({"results": serializer.data})
class VariabilityFunctionViewSet(viewsets.ModelViewSet):
    queryset = VariabilityFunction.objects.all()
    serializer_class = VariabilityFunctionSerializer
    permission_classes = [IsActive]

    def list(self, request):
        serializer = VariabilityFunctionSerializer(self.queryset, many=True)
        return Response({"results": serializer.data})
    
class FunctionParamViewSet(viewsets.ModelViewSet):
    queryset = FunctionParam.objects.all()
    serializer_class = FunctionParamSerializer
    permission_classes = [IsActive]
    
    def list(self, request):
        serializer = FunctionParamSerializer(self.queryset, many=True)
        return Response({"results": serializer.data})


class ParamAssignViewSet(viewsets.ModelViewSet):
    queryset = ParamAssign.objects.all()
    serializer_class = ParamAssignSerializer
    permission_classes = [IsActive]
    
    def list(self, request):
        serializer = ParamAssignSerializer(self.queryset, many=True)
        return Response({"results": serializer.data})
