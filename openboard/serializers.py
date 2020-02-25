from rest_framework import serializers
from .models import Board, Auth, Message


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("created_at", "modified_at")


class AuthSerializer(serializers.ModelSerializer):
    board = BoardSerializer

    class Meta:
        model = Auth
        fields = "__all__"
        read_only_fields = ("created_at", "modified_at")


class MessageSerializer(serializers.ModelSerializer):
    board = BoardSerializer

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("created_at", "modified_at")
