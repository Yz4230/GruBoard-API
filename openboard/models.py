from typing import List

from django.db import models
import nanoid
from rest_framework.exceptions import NotFound
from django.http import Http404


def createId():
    return nanoid.generate(size=8)


def createAdminAuth():
    return nanoid.generate(size=32)


def createAuth():
    return nanoid.generate(size=16)


# Create your models here.

class Board(models.Model):
    id = models.CharField(primary_key=True, max_length=8, default=createId, null=False, editable=False)
    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=True)
    admin_auth = models.CharField(max_length=32, default=createAdminAuth, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def authenticate(self, auth: str) -> None:
        auth_codes: List[str] = [self.admin_auth]
        if self.auth_set:
            auth_codes += [a.auth for a in self.auth_set.all()]
        if not auth in auth_codes:
            raise NotFound


class Auth(models.Model):
    id = models.CharField(primary_key=True, max_length=8, default=createId, null=False, editable=False)
    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=True)
    auth = models.CharField(max_length=16, default=createAuth, null=False, editable=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    id = models.CharField(primary_key=True, max_length=8, default=createId, null=False, editable=False)
    author = models.CharField(max_length=64, null=False)
    content = models.CharField(max_length=1024, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
