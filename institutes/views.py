from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Institute


class InstituteListView(ListView):
    model = Institute
    context_object_name = 'institutes'


class InstituteCreateView(CreateView):
    model = Institute
    fields = ['name', 'code', 'address', 'admission_status', 'esuvidha_status', 'contact_email', 'contact_phone']
    success_url = reverse_lazy('institutes:list')


class InstituteUpdateView(UpdateView):
    model = Institute
    fields = ['name', 'code', 'address', 'admission_status', 'esuvidha_status', 'contact_email', 'contact_phone']
    success_url = reverse_lazy('institutes:list')


class InstituteDeleteView(DeleteView):
    model = Institute
    success_url = reverse_lazy('institutes:list')
from django.shortcuts import render

# Create your views here.
