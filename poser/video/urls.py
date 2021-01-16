from django.urls import path
from . import views

urlpatterns = [
    path('monitor/', views.dance, name='swagger'),
    path('', views.index, name='index'),
]