"""
ASGI config for peer_support_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peer_support_network.settings')
django_application = get_asgi_application()
# Consumers import models, so load routes after Django initializes its apps.
from peer_support import routing

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )    
        )
    }
)
