"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
import os
import json

# Simple test view that returns plain text
def hello_world(request):
    return HttpResponse("Hello, World! Django is working.")

# Test view to show environment and settings information
def debug_info(request):
    template_dirs = settings.TEMPLATES[0]['DIRS']
    static_info = f"STATIC_URL: {settings.STATIC_URL}\nSTATIC_ROOT: {settings.STATIC_ROOT}"
    
    # Safely check if files exist
    template_files = []
    if template_dirs and os.path.exists(template_dirs[0]):
        try:
            template_files = os.listdir(template_dirs[0])
        except:
            template_files = ["Error listing template files"]
    
    # Get environment variables (excluding sensitive info)
    env_vars = {k: v for k, v in os.environ.items() 
                if not any(sensitive in k.lower() for sensitive in 
                           ['secret', 'password', 'token', 'key'])}
    
    debug_html = f"""
    <html>
    <head><title>Debug Info</title></head>
    <body>
        <h1>Django Debug Info</h1>
        <h2>Basic Info</h2>
        <p>Django Version: {settings.DJANGO_VERSION}</p>
        <p>Debug Mode: {settings.DEBUG}</p>
        
        <h2>Template Directories</h2>
        <pre>{json.dumps(template_dirs, indent=2)}</pre>
        
        <h2>Template Files</h2>
        <pre>{json.dumps(template_files, indent=2)}</pre>
        
        <h2>Static Files Configuration</h2>
        <pre>{static_info}</pre>
        
        <h2>Installed Apps</h2>
        <pre>{json.dumps(settings.INSTALLED_APPS, indent=2)}</pre>
        
        <h2>Environment Variables</h2>
        <pre>{json.dumps(env_vars, indent=2)}</pre>
    </body>
    </html>
    """
    return HttpResponse(debug_html)

# Create a simple HTML test page
def test_html(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Django Test Page</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .success { color: green; }
            .box { border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Django is working!</h1>
            <div class="box">
                <p class="success">✅ This is a test page served directly by Django</p>
                <p>If you can see this page, your basic Django setup is working correctly.</p>
                <p>Next steps:</p>
                <ul>
                    <li>Check why static files aren't loading for your React app</li>
                    <li>Verify your frontend build process</li>
                    <li>Ensure whitenoise is configured correctly</li>
                </ul>
                <p><a href="/debug/">View Debug Information</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

# Health check endpoint
def health_check(request):
    return HttpResponse('OK')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Test routes
    path('hello/', hello_world, name='hello_world'),
    path('debug/', debug_info, name='debug_info'),
    path('test/', test_html, name='test_html'),
    
    # Include your API URLs
    path('api/', include('api.urls')),
    path('market/', include('market.urls')),
    
    # Simple health check endpoint
    path('health/', health_check),
    
    # Serve the React app for all other routes
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
