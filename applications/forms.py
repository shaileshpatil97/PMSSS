from django import forms
from .models import ScholarshipApplication

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = ["course", "institute_name", "year"]
