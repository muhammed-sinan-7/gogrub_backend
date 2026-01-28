import os

import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import notifications.routing
from notifications.middleware import JWTAuthMiddleware  # << import your middleware

django_asgi_app = get_asgi_application
# Wrap the URLRouter with your JWT middleware (and optionally AuthMiddlewareStack)
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app(),
        "websocket": AuthMiddlewareStack(
            JWTAuthMiddleware(URLRouter(notifications.routing.websocket_urlpatterns))
        ),
    }
)