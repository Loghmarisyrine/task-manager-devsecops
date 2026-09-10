from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="tasks/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("", views.task_list, name="task_list"),
    path("task/new/", views.task_create, name="task_create"),
    path("task/<int:pk>/edit/", views.task_update, name="task_update"),
    path("task/<int:pk>/delete/", views.task_delete, name="task_delete"),
]
