from django.urls import path, include, re_path
from .views import ProductListView, ProductDetailView, CreateProductView, MyProductListView, LatestProductListView, export_products
import private_storage.urls

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("latest/", LatestProductListView.as_view(), name="latest"),
    path("purchased/", MyProductListView.as_view(), name="my_list"),
    path("new/", CreateProductView.as_view(), name="create"),
    path("detail/<slug:slug>/", ProductDetailView.as_view(), name="detail"),
    path('export/', export_products, name='export_products'),
    # path('private-data/<str:code>/<int:year>/<str:subdir>/<uuid:pk>/<str:filename>', ProductDownloadView.as_view(), name="file_download"),
    # path('private-data/<str:filename>', ProductDownloadView.as_view(), name="file_download"),
    re_path('^private-data/', include(private_storage.urls)),
]