"""risk_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

Examples include function views, class-based views, and including another URLconf.
"""

from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger schema view configuration using drf-yasg
schema_view = get_schema_view(
   openapi.Info(
      title="API Docs",
      default_version='v1',
      description="Documentation for Risk Manager API, a Django-based application for risk management. This documentation provides detailed information on the API endpoints, allowing for easy integration and usage.",
      terms_of_service="https://www.gnu.org/licenses/gpl-3.0.en.html",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="GPL License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Include user and incident management app URLs
    path('api/', include('user_management.urls')),
    path('api/', include('incident_management.urls')),    
    
    # Swagger documentation URLs
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),    
]
