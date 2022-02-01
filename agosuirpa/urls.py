"""agosuirpa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .settings import API_VERSION
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from django.urls import include, path
from rest_framework import routers
from experiments import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# router = routers.DefaultRouter()
# router.register(r"variations-traceability", views.VariabilityTraceabilityViewSet)
# router.register(r"generator", views.GeneratorViewSet)
# router.register(r"gui-component", views.GUIComponentViewSet)
# router.register(r"category-gui-component", views.GUIComponentCategoryViewSet)
# router.register(r"variability-configuration", views.VariabilityConfigurationViewSet)
# router.register(r"variability-function", views.VariabilityFunctionViewSet)
# router.register(r"category-variability-function", views.VariabilityFunctionCategoryViewSet)
# router.register(r"execution-configuration", views.ExecutionConfigurationViewSet)
# router.register(r"execution-result", views.ExecutionResultViewSet)

urlpatterns = [
    # path(API_VERSION, include(router.urls)),
    path(API_VERSION+'admin/', admin.site.urls),
    path(API_VERSION+'users/', include('users.urls')),
    path(API_VERSION+'experiments/', include('experiments.urls')),
    path(API_VERSION+'api-auth/', include("rest_framework.urls", namespace="rest_framework")),
    path(API_VERSION+'schema/', SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(API_VERSION+'docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(API_VERSION+'redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]