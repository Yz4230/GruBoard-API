import nanoid
from django.db import models


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


class Role(models.Model):
    ROLE_TYPES = (
        (0, "admin"),
        (1, "editor"),
        (2, "viewer")
    )

    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=True)
    auth = models.CharField(max_length=16, default=create_auth, null=False, editable=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, editable=False)
    type = models.IntegerField(choices=ROLE_TYPES, default=2)

    id = models.CharField(primary_key=True, max_length=8, default=create_id, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)


class Message(models.Model):
    author = models.CharField(max_length=64, null=False)
    author_role = models.OneToOneField(Role, on_delete=models.DO_NOTHING, null=True)
    content = models.CharField(max_length=1024, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, editable=False)

    id = models.CharField(primary_key=True, max_length=8, default=create_id, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
