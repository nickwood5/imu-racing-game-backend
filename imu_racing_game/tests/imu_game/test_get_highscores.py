from django.test import TestCase
from rest_framework import status
import imu_racing_game.models as db


class GetHighScoresTest(TestCase):
    def get_url(self, game_type: str):
        return f"/api/imu_game/get_highscores/{game_type}/"

    def test_happy_path(self):
        db.HighScore.objects.create(
            username="user1",
            game_type=db.HighScore.GameType.RACING,
            score=200,
        )
        db.HighScore.objects.create(
            username="user2",
            game_type=db.HighScore.GameType.RACING,
            score=150,
        )
        response = self.client.get(self.get_url("RACING"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        expected_response_data = {
            "high_scores": [
                {"username": "user1", "score": 200},
                {"username": "user2", "score": 150},
            ]
        }

        self.assertEqual(response_data, expected_response_data)
