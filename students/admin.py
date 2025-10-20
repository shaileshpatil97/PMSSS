from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ("id", "first_name", "last_name", "email", "phone")
	search_fields = ("first_name", "last_name", "email")

from django.contrib import admin

# Register your models here.
