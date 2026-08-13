from django.urls import path

from .views import BoardViewSet

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
    }
)

urlpatterns = [
    path("boards/", board_list, name="board-list"),
    path(
        "boards/<int:board_id>/",
        board_detail,
        name="board-detail",
    ),
]