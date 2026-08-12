from rest_framework.routers import SimpleRouter

from .views import BoardViewSet

app_name = "boards_app"

router = SimpleRouter()
router.register("boards", BoardViewSet, basename="board")

urlpatterns = router.urls