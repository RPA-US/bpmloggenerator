from django.urls import path, re_path
from . import views
from agosuirpa.urls import router

app_name = 'experiment'

router.register(r'variations', views.VariationsViewSet)

urlpatterns = [
    path('', views.ExperimentView.as_view(), name='experiment'),
    path('<id>/', views.ExperimentUpdateView.as_view(), name='experiment-update'),
    path('percentage/<int:id>/', views.check_experiment_percentage, name='experiment-percentage'),
    re_path(r'download/(?P<pk>[0-9]+)/$', views.DownloadExperiment.as_view()),
]