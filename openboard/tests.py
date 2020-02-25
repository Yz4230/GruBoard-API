from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

# Create your tests here.
from openboard.models import Board


class CrudBoard(APITestCase):
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
        board_id = res.data["id"]
        admin_auth = res.data["admin_auth"]
        print(f"New board created: {board_id=}, {admin_auth=}")

    def test_get_new_board(self):
        res: Response = self.api_client.get(
            f"/api/boards/{self.test_board_id}/?auth={self.test_board_admin_auth}",
            format="json"
        )
        self.assertIsNotNone(res)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], self.test_new_board_props["title"])
        self.assertEqual(res.data["description"], self.test_new_board_props["description"])
