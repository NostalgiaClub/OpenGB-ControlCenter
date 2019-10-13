from channels.routing import ProtocolTypeRouter, URLRouter

from ServerApp.middleware import CustomAuthMiddleware
import ServerApp.routing

application = ProtocolTypeRouter({
    'websocket': CustomAuthMiddleware(
        URLRouter(
            ServerApp.routing.websocket_urlpatterns
        )
    )
})