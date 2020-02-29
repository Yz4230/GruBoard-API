from rest_framework import serializers

from openboard.models import Role, Board, Message


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "title", "description", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("id", "title", "description", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")

    def create(self, validated_data):
        board = Board.objects.create(**validated_data)
        # Admin auth is numbered as 0.
        board.role_set.create(type=0)
        return board


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