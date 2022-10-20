from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import IsActive
from users.models import CustomUser
from .models import VariabilityFunction, VariabilityFunctionCategory, GUIComponent, GUIComponentCategory, FunctionParam, FunctionParamCategory
from .serializers import VariabilityFunctionSerializer, VariabilityFunctionCategorySerializer, GUIComponentSerializer, GUIComponentCategorySerializer, FunctionParamSerializer, FunctionParamCategorySerializer
from agosuirpa.settings import sep
from django.shortcuts import get_object_or_404
from django.db.models import Q

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


    @action(detail=False, methods=['GET'], name='id_code checker')
    def checkId(self, request):
        params = request.query_params
        if "id_code" in params:
            guiComponent = GUIComponent.objects.filter(id_code=params["id_code"])
            return Response({
                "exists": guiComponent.exists()
            })
        else:
            return Response({"message": "request was missing 'id_code' param"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        params = request.query_params
        guiCompoments = []
        user = CustomUser.objects.get(id=request.user.id)
        if "profile" in params and params["profile"] == "true":
            guiCompoments = GUIComponent.objects.filter(user=user.id)
        else:
            guiCompoments = GUIComponent.objects.filter(Q(user=user.id) | Q(preloaded=True))
        serializer = GUIComponentSerializer(guiCompoments, many=True)
        return Response({ "results": serializer.data }) 

    def create(self, request):

        try:
            user = CustomUser.objects.get(id=self.request.user.id)
        except:
            return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            gui_component_category_id = request.data.get('gui_component_category')

            if isinstance(gui_component_category_id, str):
                gui_component_category_id = int(gui_component_category_id)

            guiComponent = GUIComponent(
            id_code = request.data.get('id_code'),
            name = request.data.get('name'),
            description = request.data.get('description'),
            gui_component_category = GUIComponentCategory.objects.get(id=gui_component_category_id),
            user = user,
            image = request.data.get('image')
            )

            if user.is_superuser:
                guiComponent.preloaded = True
            guiComponent.save()

            guiComponent.filename = guiComponent.image.name.split(sep)[-1]
            guiComponent.path = guiComponent.image.name

            guiComponent.save()
            msg = 'ok, created'
            st = status.HTTP_201_CREATED
            response_content = {"message": msg, "id": guiComponent.id}

        except Exception as e:
            msg = 'Some of atributes are invalid: ' + str(e)
            st = status.HTTP_422_UNPROCESSABLE_ENTITY
            response_content = {"message": msg}
        return Response(response_content, status=st)

    def update(self, request,pk=None):
        try:
            user = CustomUser.objects.get(id=self.request.user.id)
        except:
            return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            guiComponent = get_object_or_404(GUIComponent, user=user.id, id=pk)
            guiComponent.save()
            guiComponent.id_code = request.data.get('id_code')
            guiComponent.name = request.data.get('name')
            guiComponent.filename = request.data.get('filename')
            guiComponent.path = request.data.get('path')
            guiComponent.description = request.data.get('description')
            guiComponent.gui_component_category = GUIComponentCategory.objects.get(id=request.data.get('gui_component_category'))
            guiComponent.image = request.data.get('image')
            if user.is_superuser:
                guiComponent.preloaded = True
            guiComponent.filename = guiComponent.image.name
            guiComponent.path = 'privatefiles'+sep
            guiComponent.save()
            msg = 'ok, created'
            st = status.HTTP_201_CREATED
            response_content = {"message": msg}

        except Exception as e:
            msg = 'Some of atributes are invalid: ' + str(e)
            st = status.HTTP_422_UNPROCESSABLE_ENTITY
            response_content = {"message": msg}
        return Response(response_content, status=st)

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

class FunctionParamCategoryViewSet(viewsets.ModelViewSet):
    queryset = FunctionParamCategory.objects.all()
    serializer_class = FunctionParamCategorySerializer
    permission_classes = [IsActive]
    
    def list(self, request):
        serializer = FunctionParamCategorySerializer(self.queryset, many=True)
        return Response({"results": serializer.data})
