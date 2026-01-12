from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.db.models import Count, Q 
from django.http import HttpResponse
from django.template import loader 
from .models import Task 
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from .models import Task
from .serializers import TaskSerializer

# Auth

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login')
        else:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken!")
            return redirect('register')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        # Send to email
        send_mail(
            subject='Welcome to Simple OMS',
            message=f'Hi {first_name},\n\nYour account are created successfully.\n\nThank You!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Account created successfully! Check your email.")
        return redirect('login')

    return render(request, 'register.html')


# Dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Kanban
@login_required
def board(request):
    todo = Task.objects.filter(status='todo')
    progress = Task.objects.filter(status='progress')
    done = Task.objects.filter(status='done')

    return render(request, 'board.html', {
        'todo': todo,
        'progress': progress,
        'done': done,
    })

@login_required
def update_status_ajax(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        status = request.POST.get("status")

        task = get_object_or_404(Task, id=task_id)
        task.status = status
        task.updated_by = request.user   
        task.save()

        return JsonResponse({"success": True})
    
@login_required
def user_list_view(request):
    User = get_user_model()

    users = User.objects.annotate(
        todo_count=Count(
            'updated_tasks',
            filter=Q(updated_tasks__status='todo')
        ),
        progress_count=Count(
            'updated_tasks',
            filter=Q(updated_tasks__status='progress')
        ),
        done_count=Count(
            'updated_tasks',
            filter=Q(updated_tasks__status='done')
        ),
    ).order_by('last_name', 'first_name')

    return render(request, 'crew_list.html', {
        'users': users
    })
# Throttle
# Use Postman for test
class TestThrottleView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        return Response({
            "message": "Request berhasil"
        })
    
# Other
class TaskListAPI(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LimitOffsetPagination

    # FILTERING
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter
    ]

    filterset_fields = ['status']        # ?status=todo
    search_fields = ['task_name']         # ?search=design
    ordering_fields = ['created_at']      # ?ordering=created_at
    ordering = ['-created_at']            # default sorting
