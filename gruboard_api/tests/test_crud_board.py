from rest_framework import status
from rest_framework.response import Response

from gruboard_api.tests.utils import BoardTestCase


# Create your tests here.


class ProperRequest(BoardTestCase):

    def test_create(self):
        board_props = {
            "title": "This is the test board.",
            "description": "This board is created for testing."
        }
        res = self.client.post("/api/boards/", board_props, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_read(self):
        res: Response = self.client.get(
            self.test_url,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], self.test_board_props["title"])
        self.assertEqual(res.data["description"], self.test_board_props["description"])

    def test_update(self):
        new_props = {
            "title": "Updated test board!"
        }
        res: Response = self.client.put(
            self.test_url,
            data=new_props,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], new_props["title"])

    def test_destroy(self):
        res: Response = self.client.delete(
            self.test_url,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class BadRequest(BoardTestCase):

    def test_create_with_no_props(self):
        res: Response = self.client.post("/api/boards/", format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_title(self):
        res: Response = self.client.post(
            "/api/boards/",
            {"description": "Some description..."},
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_board_list(self):
        res: Response = self.client.get("/api/boards/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_not_exist_board(self):
        res: Response = self.client.get(f"/api/boards/{'0' * 8}/?auth={'0' * 32}")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_board_with_no_auth(self):
        res: Response = self.client.get(f"/api/boards/{self.test_board.id}/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_board_with_invalid_auth(self):
        res: Response = self.client.get(f"/api/boards/{self.test_board.id}/?auth={'0' * 32}")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
