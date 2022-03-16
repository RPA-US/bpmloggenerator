from django.urls import path, re_path
from . import views

app_name = 'analyzer'

# from agosuirpa.urls import router
# router.register(r'variations', views.VariationsViewSet)

urlpatterns = [
    path('run', views.CaseStudyView.as_view(), name='run-case-study'),
]