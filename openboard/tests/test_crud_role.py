from pprint import pprint

from rest_framework import status
from rest_framework.response import Response
from .util import RoleTestCase


class ProperRequest(RoleTestCase):

    def test_create_viewer(self):
        role_props = {
            "title": "Student",
            "description": "This role is for students",
            "type": "viewer"
        }
        res: Response = self.client.post(
            f"/api/boards/{self.test_board.id}/roles/?auth={self.test_role_admin.auth}",
            role_props
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["type"], role_props["type"])

    def test_create_editor(self):
        role_props = {
            "title": "Teacher",
            "description": "This role is for teachers",
            "type": "editor"
        }
        res: Response = self.client.post(
            f"/api/boards/{self.test_board.id}/roles/?auth={self.test_role_admin.auth}",
            role_props
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["type"], role_props["type"])

    def test_create_admin(self):
        role_props = {
            "title": "School President",
            "description": "This role is for SP",
            "type": "editor"
        }
        res: Response = self.client.post(
            f"/api/boards/{self.test_board.id}/roles/?auth={self.test_role_admin.auth}",
            role_props
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["type"], role_props["type"])

    def test_read_one(self):
        res: Response = self.client.get(
            f"/api/boards/{self.test_board.id}/roles/{self.test_role_admin.id}/?auth={self.test_role_admin.auth}"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_read_list(self):
        res: Response = self.client.get(
            f"/api/boards/{self.test_board.id}/roles/?auth={self.test_role_admin.auth}"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_update(self):
        new_props = {
            "title": "Updated!",
            "type": "viewer"
        }
        res: Response = self.client.put(
            f"/api/boards/{self.test_board.id}/roles/{self.test_role_editor.id}/?auth={self.test_role_admin.auth}",
            new_props
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["type"], new_props["type"])

    def test_destroy(self):
        res: Response = self.client.delete(
            f"/api/boards/{self.test_board.id}/roles/{self.test_role_editor.id}/?auth={self.test_role_admin.auth}",
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
