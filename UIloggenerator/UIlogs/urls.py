from django.urls import path, include
from .views import CreateUIlogView, UIlogDetailView

app_name = "UIlogs"

urlpatterns = [
    path("new/", CreateUIlogView.as_view(), name="create"),
    path("detail/<slug:slug>/", UIlogDetailView.as_view(), name="detail"),
]