from rest_framework import exceptions, status
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Board, Message, Role
from .serializers import BoardSerializer, MessageSerializer, RoleSerializer


def require_auth(board_id: str, auth: str, *required_role_types) -> None:
    if not required_role_types:
        return
    board: Board = get_object_or_404(Board, id=board_id)
    if auth is None:
        raise exceptions.NotAuthenticated("The query 'auth' is required.")
    if not board.role_set.filter(auth=auth).filter(type__in=required_role_types).exists():
        raise exceptions.PermissionDenied("Your role is not allowed to access.")


class BoardViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        board_id = kwargs.get("pk")
        auth = request.query_params.get("auth")
        required_roles = []

        # Don't check if method is POST and OPTIONS
        if request.method in ("GET", "HEAD") and board_id:
            required_roles.append(Role.Types.admin)
            required_roles.append(Role.Types.editor)
            required_roles.append(Role.Types.viewer)
        elif request.method in ("PUT", "PATCH", "DELETE"):
            required_roles.append(Role.Types.admin)

        require_auth(board_id, auth, *required_roles)


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.filter(board_id=self.kwargs.get("board_pk"))

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        board_id = kwargs.get("board_pk")
        auth = request.query_params.get("auth")
        require_auth(board_id, auth, Role.Types.admin)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(board_id=self.kwargs.get("board_pk"))

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        board_id = kwargs.get("board_pk")
        auth = request.query_params.get("auth")
        if request.method == "POST":
            require_auth(
                board_id, auth,
                Role.Types.admin,
                Role.Types.editor
            )
        else:
            require_auth(
                board_id, auth,
                Role.Types.admin,
                Role.Types.editor,
                Role.Types.viewer
            )
