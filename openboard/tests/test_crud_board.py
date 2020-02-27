from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

# Create your tests here.
from openboard.models import Board


class ProperRequest(APITestCase):
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


class BadRequest(APITestCase):
    def setUp(self) -> None:
        self.api_client = APIClient()
        self.test_board_props = {
            "id": "A1B2C3D4",
            "admin_auth": "A1B2" * 8,
            "title": "Get test board",
            "description": "testing..."
        }
        board = Board.objects.create(**self.test_board_props)
        self.test_board_id = board.id
        self.test_board_admin_auth = board.admin_auth

    def test_create_with_no_props(self):
        res: Response = self.api_client.post("/api/boards/", format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_title(self):
        res: Response = self.api_client.post(
            "/api/boards/",
            {"description": "Some description..."},
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_board_list(self):
        res: Response = self.api_client.get("/api/boards/")
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_not_exist_board(self):
        res: Response = self.api_client.get(f"/api/boards/{'0' * 8}/?auth={'0' * 32}")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_board_with_no_auth(self):
        res: Response = self.api_client.get(f"/api/boards/{self.test_board_id}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
