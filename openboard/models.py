from typing import List

from django.db import models
import nanoid
from rest_framework.exceptions import NotFound
from django.http import Http404


def create_id():
    return nanoid.generate(size=8)


def create_admin_auth():
    return nanoid.generate(size=32)


def create_auth():
    return nanoid.generate(size=16)


# Create your models here.

class Board(models.Model):
    id = models.CharField(primary_key=True, max_length=8, default=create_id, null=False, editable=False)
    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=True)
    admin_auth = models.CharField(max_length=32, default=create_admin_auth, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def authenticate(self, auth: str) -> None:
        auth_codes: List[str] = [self.admin_auth]
        if self.auth_set:
            auth_codes += [a.auth for a in self.auth_set.all()]
        if auth not in auth_codes:
            raise NotFound


class Auth(models.Model):
    id = models.CharField(primary_key=True, max_length=8, default=create_id, null=False, editable=False)
    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=True)
    auth = models.CharField(max_length=16, default=create_auth, null=False, editable=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    id = models.CharField(primary_key=True, max_length=8, default=create_id, null=False, editable=False)
    author = models.CharField(max_length=64, null=False)
    content = models.CharField(max_length=1024, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
