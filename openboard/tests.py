from django.test import TestCase, Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

# Create your tests here.
from openboard.models import Board


class CURD_board(APITestCase):
    def setUp(self) -> None:
        self.api_client = APIClient()
        self.test_new_board_props = {
            "title": "Get test board",
            "description": "testing..."
        }
        board = Board.objects.create(**self.test_new_board_props)
        self.test_board_id = board.id
        self.test_board_admin_auth = board.admin_auth

    def test_create_new_board(self):
        new_board_props = {
            "title": "This is the test board.",
            "description": "This board is created for testing."
        }
        res = self.api_client.post("/api/boards/", new_board_props, format="json")
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_new_board(self):
        res: Response = self.api_client.get(
            f"/api/boards/{self.test_board_id}/?auth={self.test_board_admin_auth}",
            format="json"
        )
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], self.test_new_board_props["title"])
        self.assertEqual(res.data["description"], self.test_new_board_props["description"])

    def test_update_new_board(self):
        update_data = {
            "title": "Updated test board!"
        }
        res: Response = self.api_client.put(
            f"/api/boards/{self.test_board_id}/?auth={self.test_board_admin_auth}",
            data=update_data,
            format="json"
        )
        self.assertIsNotNone(res)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data["title"], update_data["title"])

    def test_delete_new_board(self):
        res: Response = self.api_client.delete(
            f"/api/boards/{self.test_board_id}/?auth={self.test_board_admin_auth}",
            format="json"
        )
        self.assertIsNotNone(res)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)


class CURD_message(APITestCase):
    def setUp(self) -> None:
        self.api_client = APIClient()
        self.test_new_board_props = {
            "title": "Get test board",
            "description": "testing..."
        }
        board = Board.objects.create(**self.test_new_board_props)
        self.test_board_id = board.id
        self.test_board_admin_auth = board.admin_auth
        self.test_new_message_props = {
            "author": "Bob",
            "content": "Hello World"
        }
        board.message_set.create(**self.test_new_message_props)

    def test_create_new_message(self):
        new_message_props = {
            "author": "The DRF tester",
            "content": "Can you see me?"
        }
        res = self.api_client.post(
            f"/api/boards/{self.test_board_id}/messages/?auth={self.test_board_admin_auth}",
            data=new_message_props,
            format="json"
        )
        print(res.data)
