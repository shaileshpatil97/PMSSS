from django.contrib import admin
from .models import Institute


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
	list_display = ("id", "code", "name", "admission_status", "esuvidha_status")
	search_fields = ("code", "name")
	list_filter = ("admission_status", "esuvidha_status")

from django.contrib import admin

# Register your models here.
