from django.urls import path
from .views import (
    SAGListView,
    SAGCreateView,
    SAGUpdateView,
    SAGDeleteView,
)

app_name = 'sag'

urlpatterns = [
    path('', SAGListView.as_view(), name='list'),
    path('create/', SAGCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', SAGUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', SAGDeleteView.as_view(), name='delete'),
]
