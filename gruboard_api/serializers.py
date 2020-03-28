from rest_framework import serializers

from gruboard_api.models import Role, Board, Message


class IntegerEnumChoicesField(serializers.Field):
    default_error_messages = {
        "invalid_choice": "'{input}' is not a valid choice."
    }

    def __init__(self, choices, **kwargs):
        self.choices = choices
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        assert isinstance(data, str)
        try:
            return int(self.choices[data])
        except KeyError:
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        return self.choices(value).name


class BoardSerializer(serializers.ModelSerializer):
    role_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Board
        fields = ("id", "title", "description", "role_info", "created_at", "modified_at")
        read_only_fields = ("id", "created_at", "modified_at")

    def create(self, validated_data):
        board = Board.objects.create(**validated_data)
        board.role_set.create(
            title="The Board Founder",
            description="This role was created together with board.",
            type=Role.Types.admin
        )
        return board

    def get_role_info(self, obj: Board):
        request = self.context["request"]
        if request.method == "POST":
            role = obj.role_set.order_by("created_at").first()
        else:
            role = obj.role_set.get(auth=request.query_params["auth"])
        serializer = RoleSerializer(role)
        return serializer.data


class RoleSerializer(serializers.ModelSerializer):
    type = IntegerEnumChoicesField(Role.Types)

    class Meta:
        model = Role
        fields = ("id", "title", "auth", "type", "description", "created_at", "modified_at")
        read_only_fields = ("id", "auth", "created_at", "modified_at")

    def create(self, validated_data):
        kwargs = self.context["view"].kwargs
        board_pk = kwargs["board_pk"]
        board = Board.objects.get(id=board_pk)
        return board.role_set.create(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    author_role_title = serializers.CharField(
        read_only=True,
        source="author_role.title"
    )
    author_role_type = serializers.CharField(
        read_only=True,
        source="author_role.type.name"
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "author",
            "author_role_title",
            "author_role_type",
            "content",
            "created_at",
            "modified_at"
        )
        read_only_fields = ("id", "created_at", "modified_at")

    def create(self, validated_data):
        kwargs = self.context["view"].kwargs
        request = self.context["request"]
        board_pk = kwargs["board_pk"]
        board = Board.objects.get(id=board_pk)
        validated_data["author_role"] = \
            board.role_set.get(auth=request.query_params["auth"])
        return board.message_set.create(**validated_data)
