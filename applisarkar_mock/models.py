from django.db import models

class AppliSarkarRecord(models.Model):
    aadhaar = models.CharField(max_length=12, unique=True)
    domicile_state = models.CharField(max_length=50)
    is_fraud = models.BooleanField(default=False)
    previous_scholarship = models.BooleanField(default=False)
