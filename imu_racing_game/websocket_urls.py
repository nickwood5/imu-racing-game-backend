from django.urls import path
from imu_racing_game.views.websocket.ping_consumer import PingConsumer

websocket_urlpatterns = [
    path("api/ws/ping/", PingConsumer.as_asgi()),
]
