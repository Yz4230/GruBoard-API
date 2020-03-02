from pprint import pprint

from rest_framework import exceptions, status
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Board, Message, Role
from .serializers import BoardSerializer, MessageSerializer, RoleSerializer


def require_auth(board_id: str, auth: str, *required_role_types) -> Board:
    board: Board = get_object_or_404(Board, id=board_id)
    if auth is None:
        raise exceptions.NotAuthenticated("The query 'auth' is required.")
    if not board.role_set.filter(auth=auth).filter(type__in=required_role_types).exists():
        raise exceptions.PermissionDenied("Your role is not allowed to access.")
    return board


class BoardViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.method != "POST":
            board_id = kwargs.get("pk")
            auth = request.query_params.get("auth")
            require_auth(board_id, auth, Role.Types.admin)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        role_serializer = RoleSerializer(instance=serializer.instance.role_set.first())
        response_data = {
            "created_board": serializer.data,
            "created_role": role_serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


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
