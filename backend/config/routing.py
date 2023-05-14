from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from config.ws_middleware import TokenAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddlewareStack(
            URLRouter([]),
        ),
    }
)
