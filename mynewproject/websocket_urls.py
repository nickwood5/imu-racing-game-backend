from django.urls import path
from mynewproject.views.websocket.ping_consumer import PingConsumer

websocket_urlpatterns = [
    path("api/ws/ping/", PingConsumer.as_asgi()),
]
