from django.urls import path
from .views import (
    SchemeListView, SchemeCreateView, SchemeUpdateView, SchemeDeleteView,
    ApplicationListView, ApplicationDetailView, ApplicationCreateView, ApplicationUpdateView, ApplicationDeleteView,
    ApplicationDocumentUploadView, ApplicantDashboardView, AadhaarBankLinkView,
    ProfileView, AllSchemesView, MyAppliedSchemeView, GrievanceSuggestionView, MyAppliedSchemeHistoryView
)

app_name = 'scholarships'

urlpatterns = [
    # Dashboard and info pages
    path('dashboard/', ApplicantDashboardView.as_view(), name='applicant_dashboard'),
    path('aadhaar-bank-link/', AadhaarBankLinkView.as_view(), name='aadhaar_bank_link'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('all-schemes/', AllSchemesView.as_view(), name='all_schemes'),
    path('my-applied-scheme/', MyAppliedSchemeView.as_view(), name='my_applied_scheme'),
    path('grievance-suggestion/', GrievanceSuggestionView.as_view(), name='grievance_suggestion'),
    path('my-applied-scheme-history/', MyAppliedSchemeHistoryView.as_view(), name='my_applied_scheme_history'),
    
    # Schemes
    path('schemes/', SchemeListView.as_view(), name='scheme_list'),
    path('schemes/create/', SchemeCreateView.as_view(), name='scheme_create'),
    path('schemes/<int:pk>/edit/', SchemeUpdateView.as_view(), name='scheme_edit'),
    path('schemes/<int:pk>/delete/', SchemeDeleteView.as_view(), name='scheme_delete'),

    # Applications
    path('applications/', ApplicationListView.as_view(), name='application_list'),
    path('applications/create/', ApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/edit/', ApplicationUpdateView.as_view(), name='application_edit'),
    path('applications/<int:pk>/delete/', ApplicationDeleteView.as_view(), name='application_delete'),
    path('applications/<int:pk>/upload/', ApplicationDocumentUploadView.as_view(), name='application_upload'),
]
