from django.test import TestCase
from rest_framework import status
import imu_racing_game.models as db


class SubmitHighScoreTest(TestCase):
    def get_url(self):
        return "/api/imu_game/submit_highscore/"

    def test_happy_path__new_username(self):
        request_data = {"username": "test_user", "game_type": "RACING", "score": 100}
        response = self.client.post(
            self.get_url(), data=request_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_happy_path__existing_username(self):
        mock_username = "test_user"

        high_score = db.HighScore.objects.create(
            username=mock_username, game_type=db.HighScore.GameType.RACING, score=100
        )

        new_score = 200

        request_data = {
            "username": "test_user",
            "game_type": "RACING",
            "score": new_score,
        }
        response = self.client.post(
            self.get_url(), data=request_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        high_score.refresh_from_db()

        self.assertEqual(high_score.score, new_score)

    def test_happy_path__rejects_lower_high_scores(self):
        mock_username = "test_user"
        original_score = 200

        high_score = db.HighScore.objects.create(
            username=mock_username,
            game_type=db.HighScore.GameType.RACING,
            score=original_score,
        )

        request_data = {
            "username": "test_user",
            "game_type": "RACING",
            "score": 150,
        }
        response = self.client.post(
            self.get_url(), data=request_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        high_score.refresh_from_db()

        self.assertEqual(high_score.score, original_score)

    def test_invalid_game_type_throws_error(self):
        request_data = {
            "username": "test_user",
            "game_type": "INVALID_GAME_TYPE",
            "score": 100,
        }
        response = self.client.post(
            self.get_url(), data=request_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
