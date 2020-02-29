from rest_framework import serializers

from openboard.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "title", "description", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")
