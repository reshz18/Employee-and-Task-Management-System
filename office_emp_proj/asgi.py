import os
import django
from django.core.asgi import get_asgi_application

# Ensure Django is set up before anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'office_emp_proj.settings')
django.setup()  # This ensures apps are loaded

# Now import Channels-related components
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from emp_app.routing import websocket_urlpatterns  # Import WebSocket routes

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})