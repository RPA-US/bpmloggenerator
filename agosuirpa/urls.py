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
from .system_configuration import API_VERSION
from django.contrib import admin
from django.urls import include, path, re_path
from django.shortcuts import render
from rest_framework import routers
import private_storage.urls
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.schemas import get_schema_view
# from experiments import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

@csrf_exempt
def render_react(request):
    return render(request, "index.html")

router = routers.DefaultRouter()

urlpatterns = [
    path(API_VERSION+'admin/', admin.site.urls),
    re_path(r"^$", render_react),
    re_path(r"^(?:.*)/?$", render_react),
    path(API_VERSION+'users/', include('users.urls')),
    path(API_VERSION+'experiments/', include('experiments.urls')),
    path(API_VERSION+'wizard/', include('wizard.urls')),
    path(API_VERSION+'api-auth/', include("rest_framework.urls", namespace="rest_framework")),
    path(API_VERSION+'private-media/', include('private_storage.urls')),
    path(API_VERSION+'schema/', SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(API_VERSION+'docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(API_VERSION+'redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path(API_VERSION, include(router.urls)),
]