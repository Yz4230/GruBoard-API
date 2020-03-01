from pprint import pprint

from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from .models import Board, Message, Role
from .serializers import BoardSerializer, MessageSerializer, RoleSerializer


# Create your views here.
def check_board_auth(board_id: str, auth: str) -> None:
    board: Board = get_object_or_404(Board, id=board_id)
    if auth not in board.get_all_role_auth():
        raise exceptions.NotAuthenticated()


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
            check_board_auth(kwargs.get("pk"), request.query_params.get("auth"))


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        board = Board.objects.get(id=kwargs.get("board_pk"))


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        check_board_auth(kwargs.get("board_pk"), request.query_params.get("auth"))
