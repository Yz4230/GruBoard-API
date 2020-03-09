import nanoid
from django.db import models
from enumfields import EnumIntegerField
from enum import IntEnum


def create_id():
    return nanoid.generate(size=8)


def create_auth():
    return nanoid.generate(size=16)


# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=True)

    id = models.CharField(primary_key=True, max_length=8, default=create_id, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def get_all_role_auth(self):
        return (r.auth for r in self.role_set.all())


class Role(models.Model):
    class Types(IntEnum):
        admin = 0
        editor = 1
        viewer = 2

        @classmethod
        def items(cls):
            return [(r.name, r.name.capitalize() + " role") for r in cls]

    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=True)
    auth = models.CharField(max_length=16, default=create_auth, null=False, editable=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, editable=False)
    type = EnumIntegerField(enum=Types, default=Types.viewer)

    id = models.CharField(primary_key=True, max_length=8, default=create_id, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def can_post(self) -> bool:
        return self.type in (0, 1)


class Message(models.Model):
    author = models.CharField(max_length=64, null=False)
    author_role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, null=True, related_name="+")
    content = models.CharField(max_length=1024, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, editable=False)

    id = models.CharField(primary_key=True, max_length=8, default=create_id, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
