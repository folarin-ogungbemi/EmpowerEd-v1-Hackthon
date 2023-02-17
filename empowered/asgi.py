"""
ASGI config for help_u project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "empowered"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'empowered.settings')

# This application object is used ASGI server.
django_application = get_asgi_application()

# Import websocket app here, to ensure it is loaded before
# the apps from django_application.
# pylint: disable=ungrouped-imports, wrong-import-order, wrong-import-position
from . import routing  # noqa
# pylint: disable=ungrouped-imports, wrong-import-order, wrong-import-position
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa


application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(routing.websocket_urlpatterns))),
    }
)
