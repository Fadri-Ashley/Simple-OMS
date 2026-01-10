from django.urls import path 
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('kanban/', views.board, name='board'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_page, name='register'),
    path('update-status/', views.update_status_ajax, name='update_status_ajax'),
    path('crew/', views.user_list_view, name='crew'),
    path('test-throttle/', views.TestThrottleView.as_view()),
    path('api/tasks/', views.TaskListAPI.as_view(), name='task_api'),
]