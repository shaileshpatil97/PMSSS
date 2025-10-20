from django.urls import path
from .views import (
    InstituteListView,
    InstituteCreateView,
    InstituteUpdateView,
    InstituteDeleteView,
)

app_name = 'institutes'

urlpatterns = [
    path('', InstituteListView.as_view(), name='list'),
    path('create/', InstituteCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', InstituteUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', InstituteDeleteView.as_view(), name='delete'),
]
