from django.urls import path

from .views import BoardViewSet, EmailCheckView

app_name = "boards_app"

board_list = BoardViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

board_detail = BoardViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("boards/", board_list, name="board-list"),
    path(
        "boards/<int:board_id>/",
        board_detail,
        name="board-detail",
    ),
    path(
        "email-check/",
        EmailCheckView.as_view(),
        name="email-check",
    ),
]