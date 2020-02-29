from rest_framework import serializers

from openboard.models import Auth


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = "__all__"
        read_only_fields = ("id", "created_at", "modified_at")