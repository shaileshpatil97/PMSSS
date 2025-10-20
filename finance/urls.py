from django.urls import path
from .views import (
    FinanceListView,
    FinanceCreateView,
    FinanceUpdateView,
    FinanceDeleteView,
)

app_name = 'finance'

urlpatterns = [
    path('', FinanceListView.as_view(), name='list'),
    path('create/', FinanceCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', FinanceUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', FinanceDeleteView.as_view(), name='delete'),
]
