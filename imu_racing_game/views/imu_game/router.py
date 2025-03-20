from ninja import Router
from imu_racing_game.views.imu_game.schema import (
    SubmitHighScoreRequest,
    GetHighScoresResponse,
    HighScoreListItem,
)
import imu_racing_game.models as db
from rest_framework import status
from ninja.responses import Response

imu_game_router = Router()


@imu_game_router.post("/submit_highscore/")
def submit_highscore(request, payload: SubmitHighScoreRequest):
    high_score, created = db.HighScore.objects.get_or_create(
        username=payload.username,
        game_type=payload.game_type,
        defaults={"score": payload.score},
    )

    if created:
        return Response(status=status.HTTP_204_NO_CONTENT, data=None)

    high_score.score = max(high_score.score, payload.score)
    high_score.save()

    return Response(status=status.HTTP_204_NO_CONTENT, data=None)


@imu_game_router.get("/get_highscores/{slug:game_type}/")
def get_highscores(request, game_type: str):
    print(f"Game type is {game_type}")
    high_scores = list(db.HighScore.objects.filter(game_type=game_type).all())

    high_score_data = [
        HighScoreListItem(username=high_score.username, score=high_score.score)
        for high_score in high_scores
    ]

    return GetHighScoresResponse(high_scores=high_score_data)


@imu_game_router.get("/get_highscore/{slug:game_type}/{slug:username}")
def get_highscore(request, game_type: str, username: str):
    try:
        high_score = db.HighScore.objects.get(game_type=game_type, username=username)
    except db.HighScore.DoesNotExist:
        return {"high_score": 0}

    return {"high_score": high_score.score}
