from urllib import request
from django.urls import path, re_path
from . import views

app_name = 'analyzer'

# from agosuirpa.urls import router
# router.register(r'variations', views.VariationsViewSet)

urlpatterns = [
    path('', views.CaseStudyView.as_view(), name='run-case-study'),
    path('<int:case_study_id>', views.SpecificCaseStudyView.as_view(), name='get-case-study'),
    path('<int:case_study_id>/result', views.ResultCaseStudyView.as_view(), name='get-case-study-result'),
]