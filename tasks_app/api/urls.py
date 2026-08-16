from django.urls import path

from .views import TaskViewSet

app_name = "tasks_app"

task_list = TaskViewSet.as_view(
    {
        "post": "create",
    }
)

urlpatterns = [
    path("tasks/", task_list, name="task-list"),
]