from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.template import loader 
from .models import Task 

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

        messages.info(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')

# Dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Kanban

def board(request):
    todo = Task.objects.filter(status='todo')
    progress = Task.objects.filter(status='progress')
    done = Task.objects.filter(status='done')

    return render(request, 'board.html', {
        'todo': todo,
        'progress': progress,
        'done': done,
    })