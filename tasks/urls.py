from django.urls import path

from . import views


app_name = 'tasks'


urlpatterns = [
    path('<uuid:user_id>/', views.show_all_task, name='alltasks'),
    path('<uuid:user_id>/add/', views.add, name='add'),
    
]