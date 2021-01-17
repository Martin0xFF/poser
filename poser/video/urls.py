from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='video_index'),
    path('session/', views.new_session, name='new_session'),
    path('session/<int:session_id>', views.phys_session, name='prev_session'),
    path('update/', views.update_score , name='update'),
    path('collect/', views.collect , name='collect')
]