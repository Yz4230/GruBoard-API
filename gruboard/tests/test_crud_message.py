from rest_framework import status
from rest_framework.response import Response

# noinspection DuplicatedCode
from gruboard.tests.utils import MessageTestCase


# Create your tests here.


class ProperRequest(MessageTestCase):

    def test_create(self):
        message_props = {
            "author": "The DRF tester",
            "content": "Can you see me?"
        }
        res: Response = self.client.post(
            self.test_url,
            data=message_props,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["author"], message_props["author"])
        self.assertEqual(res.data["content"], message_props["content"])

    def test_read_list(self):
        res: Response = self.client.get(
            self.test_url
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_read_one(self):
        res: Response = self.client.get(
            f"/api/boards/{self.test_board.id}/messages/{self.test_message1.id}/?auth={self.test_role_admin.auth}",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.test_message1.id)

    def test_update(self):
        new_props = {
            "author": "Mary",
            "content": "Goodnight World"
        }
        res: Response = self.client.put(
            f"/api/boards/{self.test_board.id}/messages/{self.test_message2.id}/?auth={self.test_role_admin.auth}",
            data=new_props,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["content"], new_props["content"])

    def test_destroy(self):
        res: Response = self.client.delete(
            f"/api/boards/{self.test_board.id}/messages/{self.test_message1.id}/?auth={self.test_role_admin.auth}",
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


# noinspection DuplicatedCode
class BadRequest(MessageTestCase):

    def test_create_with_no_props(self):
        res: Response = self.client.post(
            self.test_url,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_author(self):
        res: Response = self.client.post(
            self.test_url,
            {"content": "Some content..."},
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_not_exist_message(self):
        res: Response = self.client.get(
            f"/api/boards/{self.test_board.id}/messages/{'0' * 8}/?auth={self.test_role_admin.auth}"
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_message_with_no_auth(self):
        res: Response = self.client.get(
            f"/api/boards/{self.test_board.id}/messages/{self.test_message1.id}/"
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_message_with_invalid_auth(self):
        res: Response = self.client.get(
            f"/api/boards/{self.test_board.id}/messages/{self.test_message1.id}/?auth={'0' * 32}"
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
