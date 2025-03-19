from ninja import Router
from mynewproject.views.debug.schema import PingResponse

debug_router = Router()


@debug_router.get("/ping")
def ping(
    request,
):
    return PingResponse(message="Hello World!")
