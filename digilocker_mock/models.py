from django.db import models

class DigiLockerRecord(models.Model):
    aadhaar = models.CharField(max_length=12, unique=True)
    income_certificate_no = models.CharField(max_length=50)
    caste_certificate_no = models.CharField(max_length=50)
    domicile_certificate_no = models.CharField(max_length=50)
    non_creamy_layer_certificate_no = models.CharField(max_length=50, blank=True, null=True)
