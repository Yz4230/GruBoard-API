from pprint import pprint

from rest_framework import serializers

from openboard.models import Message, Board, Role
from openboard.serializers.role import RoleSerializer


class MessageSerializer(serializers.ModelSerializer):
    author_auth = serializers.CharField(
        read_only=True,
        source="author_auth.title"
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "author",
            "author_auth",
            "content",
            "created_at",
            "modified_at"
        )
        read_only_fields = ("id", "author_auth", "created_at", "modified_at")

    def create(self, validated_data):
        kwargs = self.context["view"].kwargs
        request = self.context["request"]
        board_pk = kwargs["board_pk"]
        board = Board.objects.get(id=board_pk)
        validated_data["author_role"] = \
            board.role_set.get(auth=request.query_params["auth"])
        return board.message_set.create(**validated_data)
