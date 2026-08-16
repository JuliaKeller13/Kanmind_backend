from django.urls import path

from .views import TaskViewSet

app_name = "tasks_app"

task_list = TaskViewSet.as_view(
    {
        "post": "create",
    }
)

task_detail = TaskViewSet.as_view(
    {
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("tasks/", task_list, name="task-list"),
    path(
    "tasks/<str:task_id>/",
    task_detail,
    name="task-detail",
)
]