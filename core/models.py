from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
    ]

    task_name = models.CharField(max_length=100)
    task_desc = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='todo'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
