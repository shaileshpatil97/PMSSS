from django.contrib import admin
from .models import SAG


@admin.register(SAG)
class SAGAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)

from django.contrib import admin

# Register your models here.
