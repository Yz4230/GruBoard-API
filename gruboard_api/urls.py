from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import BoardViewSet, MessageViewSet, RoleViewSet

router = DefaultRouter()
router.register(r"boards", BoardViewSet)

board_router = routers.NestedSimpleRouter(router, r"boards", lookup="board")

board_router.register(r"messages", MessageViewSet, basename="messages")
board_router.register(r"roles", RoleViewSet, basename="roles")
