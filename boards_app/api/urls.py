from django.urls import path

from .views import BoardViewSet

app_name = "boards_app"

board_list = BoardViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

urlpatterns = [
    path("boards/", board_list, name="board-list"),
]