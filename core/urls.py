from django.urls import path 
from . import views

urlpatterns = [
    path('kanban/', views.board, name='board'),
]