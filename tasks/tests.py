from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass123")

    def test_task_str(self):
        task = Task.objects.create(title="Écrire les tests", owner=self.user)
        self.assertEqual(str(task), "Écrire les tests")

    def test_default_priority_is_medium(self):
        task = Task.objects.create(title="Tâche", owner=self.user)
        self.assertEqual(task.priority, "medium")


class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="testpass123")
        self.client.login(username="bob", password="testpass123")

    def test_task_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 302)

    def test_task_list_shows_only_own_tasks(self):
        other = User.objects.create_user(username="eve", password="testpass123")
        Task.objects.create(title="À moi", owner=self.user)
        Task.objects.create(title="Pas à moi", owner=other)
        response = self.client.get(reverse("task_list"))
        self.assertContains(response, "À moi")
        self.assertNotContains(response, "Pas à moi")

    def test_create_task(self):
        response = self.client.post(reverse("task_create"), {
            "title": "Nouvelle tâche",
            "description": "Détails",
            "priority": "high",
            "is_done": False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="Nouvelle tâche").exists())

    def test_delete_task(self):
        task = Task.objects.create(title="À supprimer", owner=self.user)
        response = self.client.post(reverse("task_delete", args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())


class HealthCheckTest(TestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
