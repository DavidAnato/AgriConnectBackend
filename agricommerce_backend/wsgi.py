"""
WSGI config for agricommerce_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agricommerce_backend.settings')

application = get_wsgi_application()

# Create superuser if it does not exist
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@agricommerce.com",
            password="admin1234"
        )
        logging.info("Superuser 'admin' created successfully.")
    else:
        logging.info("Superuser 'admin' already exists.")
except Exception as e:
    # Never prevent the app from starting if superuser creation fails
    logging.warning("Failed to create superuser: %s", e)
    pass

# Keepalive interne: active via ENABLE_KEEPALIVE=true
if os.getenv('ENABLE_KEEPALIVE', 'false').lower() == 'true':
    try:
        from utils.keepalive import start_keepalive
        # 14 minutes par défaut
        start_keepalive()
    except Exception:
        # Ne jamais empêcher le démarrage de l’app si le keepalive échoue
        pass
