from rest_framework import serializers

from openboard.models import Board


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
