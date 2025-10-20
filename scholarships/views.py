from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
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
    fields = ['applicant_name', 'applicant_email', 'scheme', 'institute', 'remarks']
    success_url = reverse_lazy('scholarships:application_list')


class ApplicationUpdateView(UpdateView):
    model = Application
    fields = ['applicant_name', 'applicant_email', 'scheme', 'institute', 'remarks']
    success_url = reverse_lazy('scholarships:application_list')


class ApplicationDeleteView(DeleteView):
    model = Application
    success_url = reverse_lazy('scholarships:application_list')


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
