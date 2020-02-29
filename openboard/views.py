from pprint import pprint

from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from .models import Board, Message
from .serializers import BoardSerializer, MessageSerializer


# Create your views here.
def check_board_auth(board_id: str, auth: str) -> None:
    board: Board = get_object_or_404(Board, id=board_id)
    auth_list = [a.auth for a in board.role_set.all()]
    if auth not in auth_list:
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


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        check_board_auth(kwargs.get("board_pk"), request.query_params.get("auth"))
