from django.contrib import admin
from .models import Scheme, Application, ApplicationDocument


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "department", "is_active")
    search_fields = ("name", "department")
    list_filter = ("department", "is_active")


class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "applicant_name", "scheme", "status")
    list_filter = ("status", "scheme")
    search_fields = ("applicant_name", "applicant_email")
    inlines = [ApplicationDocumentInline]


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "doc_type", "uploaded_at")
from django.contrib import admin

# Register your models here.
