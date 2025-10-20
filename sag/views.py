from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import SAG


class SAGListView(ListView):
    model = SAG
    context_object_name = 'sags'


class SAGCreateView(CreateView):
    model = SAG
    fields = ['name', 'description']
    success_url = reverse_lazy('sag:list')


class SAGUpdateView(UpdateView):
    model = SAG
    fields = ['name', 'description']
    success_url = reverse_lazy('sag:list')


class SAGDeleteView(DeleteView):
    model = SAG
    success_url = reverse_lazy('sag:list')
from django.shortcuts import render

# Create your views here.
