from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import FinanceRecord


class FinanceListView(ListView):
    model = FinanceRecord
    context_object_name = 'records'


class FinanceCreateView(CreateView):
    model = FinanceRecord
    fields = ['student_name', 'amount', 'status', 'remarks']
    success_url = reverse_lazy('finance:list')


class FinanceUpdateView(UpdateView):
    model = FinanceRecord
    fields = ['student_name', 'amount', 'status', 'remarks']
    success_url = reverse_lazy('finance:list')


class FinanceDeleteView(DeleteView):
    model = FinanceRecord
    success_url = reverse_lazy('finance:list')
from django.shortcuts import render

# Create your views here.
