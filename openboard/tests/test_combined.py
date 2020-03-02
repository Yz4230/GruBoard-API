from pprint import pprint

from rest_framework.response import Response
from rest_framework import status

from .util import CombinedTestCase
from openboard.models import Board


class ProperScenario(CombinedTestCase):

    def test_1(self):
        res: Response = self.client.post(
            f"/api/boards/",
            {"title": self.faker.company(),
             "description": self.faker.text()}
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        board_id = res.data["created_board"]["id"]
        admin_auth = res.data["created_admin"]["auth"]
