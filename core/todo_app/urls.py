from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('update/<int:pk>/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/mark_done/', views.MarkDoneView.as_view(), name='mark_done'),
]