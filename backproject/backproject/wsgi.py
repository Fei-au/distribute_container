"""
WSGI config for backproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backproject.settings")

# Fetch google security credentials
# from google.auth import default
# from google.auth.transport.requests import Request
# credentials, project = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])


application = get_wsgi_application()
