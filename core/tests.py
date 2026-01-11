from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):

    def setUp(self):
        """Dijalankan sebelum setiap test"""
        self.task = Task.objects.create(
            task_name="Belajar Django",
            task_desc="Belajar unit testing Django",
            status="todo"
        )

    def test_task_created(self):
        """Test apakah task berhasil dibuat"""
        self.assertEqual(self.task.task_name, "Belajar Django")
        self.assertEqual(self.task.status, "todo")

    def test_default_status(self):
        """Test default status"""
        task = Task.objects.create(task_name="Task baru")
        self.assertEqual(task.status, "todo")

    def test_str_method(self):
        """Test method __str__"""
        self.assertEqual(str(self.task), "Belajar Django")

    def test_status_choices(self):
        """Test status hanya boleh sesuai choices"""
        valid_status = [choice[0] for choice in Task.STATUS_CHOICES]
        self.assertIn(self.task.status, valid_status)
