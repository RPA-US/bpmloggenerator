from django.urls import path, re_path
from . import views
from agosuirpa.urls import router

app_name = 'experiment'

router.register(r'variations', views.VariationsViewSet)

urlpatterns = [
    path('', views.ExperimentView.as_view(), name='experiment'),
    path('<id>/', views.ExperimentUpdate.as_view(), name='experiment_update'),
    re_path(r'download/(?P<pk>[0-9]+)/$', views.DownloadExperiment.as_view()),
    # path('<id>/', views.ExperimentUpdate.as_view(), name='edit'),
    # path('<id>/delete', views.SoftDeleteExperimentAPIView.as_view(),name='delete'),
    # path('list', views.ListActiveExperimentAPIView.as_view(), name='list_active'),
    # path('pagination', views.ListPaginatedExperimentAPIView.as_view(), name='pagination'),
]