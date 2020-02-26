from rest_framework import viewsets, mixins
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Board, Message
from .serializers import BoardSerializer, MessageSerializer


# Create your views here.


class BoardViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def retrieve(self, request: Request, *args, **kwargs):
        board = Board.objects.get(id=self.kwargs["pk"])
        serializer = self.get_serializer(board)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        board = Board.objects.get(id=kwargs["board_pk"])
        auth = request.query_params.get("auth", None)
        board.authenticate(auth)
