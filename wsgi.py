import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DealFlowAI.settings_vercel')

# Get the WSGI application
application = get_wsgi_application()

# For Vercel serverless functions
app = application 