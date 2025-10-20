"""
URL configuration for pmsss_portal project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('students/', include('students.urls')),
    path('institutes/', include('institutes.urls')),
    path('sag/', include('sag.urls')),
    path('finance/', include('finance.urls')),
    path('scholarships/', include('scholarships.urls')),
    path('api/', include('pmsss_portal.api')),
]

# Static and media in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
