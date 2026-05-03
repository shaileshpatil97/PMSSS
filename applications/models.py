import uuid
from django.db import models
from accounts.models import User
from django.conf import settings


class ScholarshipScheme(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=150)
    min_income = models.IntegerField()
    caste = models.CharField(max_length=50)
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class ScholarshipApplication(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("UNDER_SCRUTINY", "Under Scrutiny"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("CANCELLED", "Cancelled"),
        ("GIVEUP", "Give Up"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=200)
    year = models.IntegerField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="DRAFT")
    created_at = models.DateTimeField(auto_now_add=True)



class ApplicationDocuments(models.Model):
    application = models.OneToOneField(ScholarshipApplication, on_delete=models.CASCADE)
    income_cert = models.CharField(max_length=50)
    caste_cert = models.CharField(max_length=50)
    domicile_cert = models.CharField(max_length=50)
    non_creamy_layer_cert = models.CharField(max_length=50, blank=True, null=True)
    verified = models.BooleanField(default=False)


    
class Notification(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

