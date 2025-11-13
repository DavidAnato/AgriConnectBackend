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

# Configure logger
logger = logging.getLogger(__name__)

# Créer un superuser si inexistant
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # On vérifie selon le champ principal
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@agriconnect.com')

    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            email=admin_email,
            password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin1234'),
            first_name='Admin',
            last_name='User',
            phone_number='0000000000',  # si ton modèle le requiert
            is_active=True
        )
        logger.info("Superuser created successfully.")
except Exception as e:
    logger.error("Failed to create superuser: %s", e)
    # Never prevent the app from starting if superuser creation fails
    pass

# Keepalive interne: active via ENABLE_KEEPALIVE=true
if os.getenv('ENABLE_KEEPALIVE', 'false').lower() == 'true':
    try:
        from utils.keepalive import start_keepalive
        # 14 minutes par défaut
        start_keepalive()
        logger.info("Keepalive started.")
    except Exception as e:
        logger.error("Failed to start keepalive: %s", e)
        # Ne jamais empêcher le démarrage de l’app si le keepalive échoue
        pass
