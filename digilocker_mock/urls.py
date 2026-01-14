from django.urls import path
from .views import fetch_docs

urlpatterns = [
    path("fetch/<str:aadhaar>/", fetch_docs),
]
