"""
WSGI config for agricommerce_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agricommerce_backend.settings')

application = get_wsgi_application()

# Keepalive interne: active via ENABLE_KEEPALIVE=true
if os.getenv('ENABLE_KEEPALIVE', 'false').lower() == 'true':
    try:
        from utils.keepalive import start_keepalive
        # 14 minutes par défaut
        start_keepalive()
    except Exception:
        # Ne jamais empêcher le démarrage de l’app si le keepalive échoue
        pass
