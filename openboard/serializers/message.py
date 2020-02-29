from rest_framework import serializers

from openboard.models import Message, Board


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("id", "created_at", "modified_at")

    def create(self, validated_data):
        kwargs = self.context["view"].kwargs
        board_pk = kwargs["board_pk"]
        board = Board.objects.get(id=board_pk)
        return board.message_set.create(**validated_data)