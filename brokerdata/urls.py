from django.urls import path
from .views import index, ChartData, download_csv

urlpatterns = [
    path('', index, name='index'),
    path('api/chartdata/<str:topic>/', ChartData.as_view(), name='chartdata'),
    path('download/<str:topic>/', download_csv, name='download_csv'),
]
