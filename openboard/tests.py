from pprint import pprint

from django.test import TestCase, Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

# Create your tests here.
from openboard.models import Board


class CurdBoard(APITestCase):
    def setUp(self) -> None:
        self.api_client = APIClient()
        self.test_board_props = {
            "title": "Get test board",
            "description": "testing..."
        }
        board = Board.objects.create(**self.test_board_props)
        self.test_board_id = board.id
        self.test_board_admin_auth = board.admin_auth

    def test_create(self):
        board_props = {
            "title": "This is the test board.",
            "description": "This board is created for testing."
        }
        res = self.api_client.post("/api/boards/", board_props, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_read(self):
        res: Response = self.api_client.get(
            f"/api/boards/{self.test_board_id}/?auth={self.test_board_admin_auth}",
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], self.test_board_props["title"])
        self.assertEqual(res.data["description"], self.test_board_props["description"])

    def test_update(self):
        new_props = {
            "title": "Updated test board!"
        }
        res: Response = self.api_client.put(
            f"/api/boards/{self.test_board_id}/?auth={self.test_board_admin_auth}",
            data=new_props,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], new_props["title"])

    def test_destroy(self):
        res: Response = self.api_client.delete(
            f"/api/boards/{self.test_board_id}/?auth={self.test_board_admin_auth}",
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class CurdMessage(APITestCase):
    def setUp(self) -> None:
        self.api_client = APIClient()
        self.test_board_props = {
            "title": "Get test board",
            "description": "testing..."
        }
        board = Board.objects.create(**self.test_board_props)
        self.test_board_id = board.id
        self.test_board_admin_auth = board.admin_auth
        self.test_url = f"/api/boards/{self.test_board_id}/messages/?auth={self.test_board_admin_auth}"
        self.test_message1 = board.message_set.create(author="Bob", content="Hello World!")
        self.test_message2 = board.message_set.create(author="Mary", content="Bye World!")

    def test_create(self):
        message_props = {
            "author": "The DRF tester",
            "content": "Can you see me?"
        }
        res: Response = self.api_client.post(
            self.test_url,
            data=message_props,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["author"], message_props["author"])
        self.assertEqual(res.data["content"], message_props["content"])

    def test_read_list(self):
        res: Response = self.api_client.get(
            self.test_url
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_read_one(self):
        res: Response = self.api_client.get(
            f"/api/boards/{self.test_board_id}/messages/{self.test_message1.id}/?auth={self.test_board_admin_auth}"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.test_message1.id)

    def test_update(self):
        new_props = {
            "author": "Mary",
            "content": "Goodnight World"
        }
        res: Response = self.api_client.put(
            f"/api/boards/{self.test_board_id}/messages/{self.test_message2.id}/?auth={self.test_board_admin_auth}",
            data=new_props,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["content"], new_props["content"])

    def test_destroy(self):
        res: Response = self.api_client.delete(
            f"/api/boards/{self.test_board_id}/messages/{self.test_message1.id}/?auth={self.test_board_admin_auth}",
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
