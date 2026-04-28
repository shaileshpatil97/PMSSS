from django.urls import path
from .views import verify_student

urlpatterns = [
    path("verify/<str:aadhaar>/", verify_student),
]
