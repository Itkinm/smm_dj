from django.urls import path
from django.conf.urls import url, include

from . import views

app_name = 'socnet'
urlpatterns = [
    path('', views.index, name='index'),
    path('platform/<str:platform_name>/', views.platform, name='platform'),
    path('shtab/<str:shtab_name>/', views.shtab, name='shtab'),
    ]