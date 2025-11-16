from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView, TemplateView
from django import forms
from .models import Scheme, Application, ApplicationDocument
from django.db.models import Q


class SchemeListView(ListView):
    model = Scheme
    context_object_name = 'schemes'


class SchemeCreateView(CreateView):
    model = Scheme
    fields = ['name', 'department', 'description', 'is_active', 'start_date', 'end_date']
    success_url = reverse_lazy('scholarships:scheme_list')


class SchemeUpdateView(UpdateView):
    model = Scheme
    fields = ['name', 'department', 'description', 'is_active', 'start_date', 'end_date']
    success_url = reverse_lazy('scholarships:scheme_list')


class SchemeDeleteView(DeleteView):
    model = Scheme
    success_url = reverse_lazy('scholarships:scheme_list')


class ApplicationListView(ListView):
    model = Application
    context_object_name = 'applications'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(
                Q(applicant_name__icontains=q)
                | Q(applicant_email__icontains=q)
                | Q(student__first_name__icontains=q)
                | Q(student__last_name__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs


class ApplicationDetailView(DetailView):
    model = Application


class ApplicationCreateView(CreateView):
    model = Application
    fields = ['student', 'applicant_name', 'applicant_email', 'scheme', 'institute', 'remarks']
    success_url = reverse_lazy('scholarships:application_list')
    template_name = 'scholarships/application_form_wizard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_step'] = self.request.GET.get('step', 'personal')
        return ctx


class ApplicationUpdateView(UpdateView):
    model = Application
    fields = ['applicant_name', 'applicant_email', 'scheme', 'institute', 'remarks']
    success_url = reverse_lazy('scholarships:application_list')


class ApplicationDeleteView(DeleteView):
    model = Application
    success_url = reverse_lazy('scholarships:application_list')


class ApplicantDashboardView(ListView):
    model = Application
    template_name = 'scholarships/applicant_dashboard.html'
    context_object_name = 'my_applications'

    def get_queryset(self):
        # Filter by current user if you have authentication, for now return all
        return Application.objects.all().order_by('-id')[:5]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile_completeness'] = 100  # Calculate based on user profile fields
        ctx['suggested_schemes'] = Scheme.objects.filter(is_active=True)[:10]
        return ctx


class AadhaarBankLinkView(TemplateView):
    template_name = 'scholarships/aadhaar_bank_link.html'


class ProfileView(TemplateView):
    template_name = 'scholarships/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile_completeness'] = 100
        ctx['current_step'] = self.request.GET.get('step', 'personal')
        return ctx


class AllSchemesView(ListView):
    model = Scheme
    template_name = 'scholarships/all_schemes.html'
    context_object_name = 'schemes'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        dept = self.request.GET.get('department')
        scheme_name = self.request.GET.get('scheme_name')
        if dept:
            qs = qs.filter(department=dept)
        if scheme_name:
            qs = qs.filter(id=scheme_name)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['departments'] = Scheme.objects.values_list('department', flat=True).distinct()
        return ctx


class MyAppliedSchemeView(ListView):
    model = Application
    template_name = 'scholarships/my_applied_scheme.html'
    context_object_name = 'applications'

    def get_queryset(self):
        # Filter by current user in production
        return Application.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['under_scrutiny'] = self.get_queryset().filter(status__in=['submitted', 'institute_verified'])
        ctx['approved'] = self.get_queryset().filter(status='department_approved')
        ctx['rejected'] = self.get_queryset().filter(status='rejected')
        ctx['disbursed'] = self.get_queryset().filter(status='disbursed')
        return ctx


class GrievanceSuggestionView(TemplateView):
    template_name = 'scholarships/grievance_suggestion.html'


class MyAppliedSchemeHistoryView(TemplateView):
    template_name = 'scholarships/my_applied_scheme_history.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['academic_years'] = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
        return ctx


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ['doc_type', 'file']


class ApplicationDocumentUploadView(FormView):
    template_name = 'scholarships/application_upload.html'
    form_class = DocumentUploadForm

    def form_valid(self, form):
        application = Application.objects.get(pk=self.kwargs['pk'])
        doc = form.save(commit=False)
        doc.application = application
        doc.save()
        self.success_url = reverse_lazy('scholarships:application_detail', kwargs={'pk': application.pk})
        return super().form_valid(form)
from django.shortcuts import render

# Create your views here.
