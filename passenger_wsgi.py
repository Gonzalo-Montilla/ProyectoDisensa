import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'securebusinessapp'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "securebusinessapp.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()