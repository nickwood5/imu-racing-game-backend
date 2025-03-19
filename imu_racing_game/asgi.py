"""
ASGI config for imu_racing_game project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from imu_racing_game.websocket_urls import websocket_urlpatterns

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imu_racing_game.settings")

asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": URLRouter(
            websocket_urlpatterns,
        ),
    }
)
