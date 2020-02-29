from rest_framework.test import APITestCase

from openboard.models import Role, Board, Message


def create_test_board(board_props=None, role_props=None) -> (Board, Role):
    """
    Create test board with the properties if they are specified.
    :param board_props: properties for test board
    :param role_props: properties for test role
    :return: Board and Auth created instances
    """
    board = Board.objects.create(**(board_props or {}))
    role = board.role_set.create(**(role_props or {}))
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
        self.test_role_props = {
            "id": "authA1B2",
            "title": "Role used in auth",
            "description": "testing..."
        }
        self.test_board, self.test_role = create_test_board(
            self.test_board_props,
            self.test_role_props
        )
        self.test_url = f"/api/boards/{self.test_board.id}/?auth={self.test_role.auth}"


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
        self.test_message1 = create_test_message(self.test_board.id, self.test_message1_props)
        self.test_message2 = create_test_message(self.test_board.id, self.test_message2_props)
        self.test_url = f"/api/boards/{self.test_board.id}/messages/?auth={self.test_role.auth}"
