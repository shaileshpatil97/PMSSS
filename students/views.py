from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Student


class StudentListView(ListView):
    model = Student
    context_object_name = 'students'


class StudentCreateView(CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'email', 'phone', 'dob']
    success_url = reverse_lazy('students:list')


class StudentUpdateView(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'email', 'phone', 'dob']
    success_url = reverse_lazy('students:list')


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('students:list')

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Student


class StudentListView(ListView):
    model = Student
    context_object_name = 'students'


class StudentCreateView(CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'email', 'phone', 'dob']
    success_url = reverse_lazy('students:list')


class StudentUpdateView(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'email', 'phone', 'dob']
    success_url = reverse_lazy('students:list')


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('students:list')
from django.shortcuts import render

# Create your views here.
