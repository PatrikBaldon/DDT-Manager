"""
Settings package for DDT Application.
"""

import os

# Get the environment variable to determine which settings to use
ENVIRONMENT = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.development')

if 'production' in ENVIRONMENT:
    from .production import *
elif 'testing' in ENVIRONMENT:
    from .testing import *
else:
    from .development import *
