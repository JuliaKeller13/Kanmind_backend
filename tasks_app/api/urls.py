from django.urls import path

from .views import (
    AssignedTasksView,
    ReviewingTasksView,
    TaskCommentDetailView,
    TaskCommentListCreateView,
    TaskViewSet,
)

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
        "tasks/assigned-to-me/",
        AssignedTasksView.as_view(),
        name="assigned-to-me",
    ),
    path(
        "tasks/reviewing/",
        ReviewingTasksView.as_view(),
        name="reviewing",
    ),
    path(
        "tasks/<str:task_id>/comments/",
        TaskCommentListCreateView.as_view(),
        name="task-comments",
    ),
    path(
        "tasks/<str:task_id>/comments/<str:comment_id>/",
        TaskCommentDetailView.as_view(),
        name="task-comment-detail",
    ),
    path(
        "tasks/<str:task_id>/",
        task_detail,
        name="task-detail",
    ),
]