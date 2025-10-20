from django.contrib import admin
from .models import FinanceRecord


@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):
	list_display = ("id", "student_name", "amount", "status")
	list_filter = ("status",)
	search_fields = ("student_name",)

from django.contrib import admin

# Register your models here.
