from django.urls import include, path
from rest_framework.routers import DefaultRouter
from students.api import router as students_router
from institutes.api import router as institutes_router
from sag.api import router as sag_router
from finance.api import router as finance_router

router = DefaultRouter()

# Extend the main router with app-specific routers
for r in (students_router, institutes_router, sag_router, finance_router):
    for prefix, viewset, basename in getattr(r, 'registry', []):
        router.register(prefix, viewset, basename=basename)

urlpatterns = [
    path('', include(router.urls)),
]
