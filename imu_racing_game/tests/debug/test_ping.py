from django.test import TestCase
from rest_framework import status


class PingTest(TestCase):
    def get_url(self):
        return "/api/debug/ping"

    def test_happy_path(self):
        response = self.client.get(self.get_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
