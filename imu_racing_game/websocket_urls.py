from django.urls import path
from imu_racing_game.views.websocket.ping_consumer import PingConsumer
from imu_racing_game.views.websocket.image_consumer import (
    ImageUploadConsumer,
    ImageBroadcastConsumer,
)
from imu_racing_game.views.websocket.imu_consumer import (
    IMUBroadcastConsumer,
    IMUUploadConsumer,
)
from imu_racing_game.views.websocket.imu_game_consumer import (
    IMUGameBroadcastConsumer,
    IMUGameUploadConsumer,
)

websocket_urlpatterns = [
    path("api/ws/ping/", PingConsumer.as_asgi()),
    path("api/ws/image/upload/", ImageUploadConsumer.as_asgi()),
    path("api/ws/image/broadcast/", ImageBroadcastConsumer.as_asgi()),
    path("api/ws/imu/<slug:id>/upload/", IMUUploadConsumer.as_asgi()),
    path("api/ws/imu/<slug:id>/broadcast/", IMUBroadcastConsumer.as_asgi()),
    path(
        "api/ws/imu_game/<slug:game_id>/broadcast/", IMUGameBroadcastConsumer.as_asgi()
    ),
    path(
        "api/ws/imu_game/<slug:game_id>/<slug:player_id>/upload/",
        IMUGameUploadConsumer.as_asgi(),
    ),
]
