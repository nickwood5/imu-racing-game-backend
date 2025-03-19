from ninja import Router
from imu_racing_game.views.debug.schema import PingResponse

debug_router = Router()


@debug_router.get("/ping")
def ping(
    request,
):
    return PingResponse(message="Hello World!")
