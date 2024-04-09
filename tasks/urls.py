from django.urls import path

from . import views


app_name = 'tasks'


urlpatterns = [
    path('<uuid:user_id>/', views.show_all_task, name='alltasks'),
    path('<uuid:user_id>/<uuid:task_id>/detail/', views.detail, name='detail'),
    path('<uuid:user_id>/<uuid:task_id>/edit/', views.edit, name='edit'),
    path('<uuid:user_id>/<uuid:task_id>/delete/', views.delete, name='delete'),
    path('<uuid:user_id>/add/', views.add, name='add'),

]