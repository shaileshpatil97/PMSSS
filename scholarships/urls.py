from django.urls import path
from .views import (
    SchemeListView, SchemeCreateView, SchemeUpdateView, SchemeDeleteView,
    ApplicationListView, ApplicationDetailView, ApplicationCreateView, ApplicationUpdateView, ApplicationDeleteView,
    ApplicationDocumentUploadView
)

app_name = 'scholarships'

urlpatterns = [
    path('schemes/', SchemeListView.as_view(), name='scheme_list'),
    path('schemes/create/', SchemeCreateView.as_view(), name='scheme_create'),
    path('schemes/<int:pk>/edit/', SchemeUpdateView.as_view(), name='scheme_edit'),
    path('schemes/<int:pk>/delete/', SchemeDeleteView.as_view(), name='scheme_delete'),

    path('applications/', ApplicationListView.as_view(), name='application_list'),
    path('applications/create/', ApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/edit/', ApplicationUpdateView.as_view(), name='application_edit'),
    path('applications/<int:pk>/delete/', ApplicationDeleteView.as_view(), name='application_delete'),
    path('applications/<int:pk>/upload/', ApplicationDocumentUploadView.as_view(), name='application_upload'),
]
