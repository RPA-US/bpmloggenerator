from agosuirpa.urls import router
# from django.urls import path, re_path
from .views import FunctionParamViewSet, VariabilityFunctionCategoryViewSet, VariabilityFunctionViewSet, GUIComponentCategoryViewSet, GUIComponentViewSet, FunctionParamCategoryViewSet

app_name = 'wizard'

router.register(r'gui-component', GUIComponentViewSet)
router.register(r'category-gui-component', GUIComponentCategoryViewSet)
router.register(r'variability-function', VariabilityFunctionViewSet)
router.register(r'category-variability-function', VariabilityFunctionCategoryViewSet)
router.register(r'function-param-category', FunctionParamCategoryViewSet)
router.register(r'function-param', FunctionParamViewSet)

urlpatterns = [
#     path('gui-component', views.GUIComponentViewSet, name='gui_component'),
#     path('category-gui-component', views.GUIComponentCategoryViewSet, name='category_gui_component'),
#     path('variability-function', views.VariabilityFunctionViewSet, name='variability_function'),
#     path('category-variability-function', views.VariabilityFunctionCategoryViewSet, name='category_variability_function'),
]