from ninja import Schema
from enum import Enum
import imu_racing_game.models as db
from typing import List


class GameTypeEnum(str, Enum):
    RACING = db.HighScore.GameType.RACING


class SubmitHighScoreRequest(Schema):
    username: str
    game_type: GameTypeEnum
    score: int


class HighScoreListItem(Schema):
    username: str
    score: int


class GetHighScoresResponse(Schema):
    high_scores: List[HighScoreListItem]
