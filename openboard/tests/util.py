from rest_framework.test import APITestCase
from faker import Faker
from faker.providers import job, company
from openboard.models import Role, Board, Message
from random import choice


def create_test_board(board_props=None, role_props=None) -> (Board, Role):
    """
    Create test board with the properties if they are specified.
    :param board_props: properties for test board
    :param role_props: properties for test role
    :return: Board and Role created instances
    """
    board = Board.objects.create(**(board_props or {}))
    # Type 0 means admin
    role = board.role_set.create(**(role_props or {}), type=0)
    return board, role


def create_test_message(board_id, message_props=None) -> Message:
    board = Board.objects.get(id=board_id)
    return board.message_set.create(**(message_props or {}))


class BoardTestCase(APITestCase):

    def setUp(self) -> None:
        self.test_board_props = {
            "id": "boardA1B",
            "title": "Board used in test",
            "description": "testing..."
        }
        self.test_role_admin_props = {
            "id": "authA1B2",
            "title": "Role used in auth",
            "description": "testing..."
        }
        self.test_board, self.test_role_admin = create_test_board(
            self.test_board_props,
            self.test_role_admin_props
        )
        self.test_url = f"/api/boards/{self.test_board.id}/?auth={self.test_role_admin.auth}"


class MessageTestCase(BoardTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.test_message1_props = {
            "author": "Bob",
            "content": "Can you see me?"
        }
        self.test_message2_props = {
            "author": "Mary",
            "content": "Cannot you see me?"
        }
        self.test_message1 = self.test_board.message_set.create(**self.test_message1_props)
        self.test_message2 = self.test_board.message_set.create(**self.test_message2_props)
        self.test_url = f"/api/boards/{self.test_board.id}/messages/?auth={self.test_role_admin.auth}"


class RoleTestCase(BoardTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.test_role_editor_props = {
            "id": "editorA1",
            "title": "Test editor role",
            "description": "Testing...",
            "type": Role.RoleTypes.editor
        }
        self.test_role_viewer_props = {
            "id": "viewerA1",
            "title": "Test viewer role",
            "description": "Testing...",
            "type": Role.RoleTypes.viewer
        }
        self.test_role_editor = self.test_board.role_set.create(**self.test_role_editor_props)
        self.test_role_viewer = self.test_board.role_set.create(**self.test_role_viewer_props)
        self.test_url = None


class CombinedTestCase(APITestCase):

    def setUp(self) -> None:
        self.faker = Faker(["ja_JP"])
        self.faker.add_provider(job)
        self.faker.add_provider(company)

    def create_board_props(self, count):
        ret = []
        for i in range(count):
            props = {
                "id": str(i).zfill(8),
                "title": self.faker.company(),
                "description": self.faker.text()
            }
            ret.append(props)
        return ret

    def create_role_props(self, count):
        ret = []
        for i in range(count):
            props = {
                "id": str(i).zfill(8),
                "title": self.faker.job(),
                "description": self.faker.text(),
                "auth": str(i).center(16, '0'),
                "type": choice((Role.RoleTypes.admin, Role.RoleTypes.viewer, Role.RoleTypes.viewer))
            }
            ret.append(props)
        return ret

    def create_message_props(self, count):
        ret = []
        for i in range(count):
            props = {
                "id": str(i).zfill(8),
                "author": self.faker.name(),
                "content": self.faker.text()
            }
            ret.append(props)
        return ret
