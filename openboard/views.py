from pprint import pprint

from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from .models import Board, Message, Role
from .serializers import BoardSerializer, MessageSerializer, RoleSerializer


# Create your views here.
def check_board_auth(board_id: str, auth: str) -> Board:
    board: Board = get_object_or_404(Board, id=board_id)
    if auth is None:
        raise exceptions.NotAuthenticated(
            "The query 'auth' is required."
        )
    if auth not in board.get_all_role_auth():
        raise exceptions.PermissionDenied(
            "The auth is invalid."
        )
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
            check_board_auth(board_id, auth)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        board_id = kwargs.get("board_pk")
        auth = request.query_params.get("auth")
        board = check_board_auth(board_id, auth)

        role = board.role_set.get(auth=auth)
        if role.type != Role.RoleTypes.admin:
            raise exceptions.PermissionDenied(
                "Only admin can crud auth."
            )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        board_id = kwargs.get("board_pk")
        auth = request.query_params.get("auth")
        check_board_auth(board_id, auth)
