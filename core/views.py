from django.shortcuts import render
from .models import Task 

def board(request):
    todo = Task.objects.filter(status='todo')
    progress = Task.objects.filter(status='progress')
    done = Task.objects.filter(status='done')

    return render(request, 'board.html', {
        'todo': todo,
        'progress': progress,
        'done': done,
    })