import uuid
from django.db import models
from accounts.models import User
from applications.models import ScholarshipApplication

class Institute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Login account (role = INSTITUTE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    institute_code = models.CharField(max_length=50, unique=True)
    institute_name = models.CharField(max_length=200)

    address = models.TextField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.institute_name


class InstituteVerification(models.Model):
    application = models.OneToOneField(
        ScholarshipApplication,
        on_delete=models.CASCADE
    )
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE
    )

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    remarks = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.application.id} - {self.status}"


class InstituteStudent(models.Model):
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE
    )
    aadhaar = models.CharField(max_length=12)
    student_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year = models.IntegerField()

    class Meta:
        unique_together = ("institute", "aadhaar")

    def __str__(self):
        return f"{self.student_name} ({self.aadhaar})"

class InstituteStudent(models.Model):
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE
    )
    aadhaar = models.CharField(max_length=12)
    student_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year = models.IntegerField()

    class Meta:
        unique_together = ("institute", "aadhaar")

    def __str__(self):
        return f"{self.student_name} ({self.aadhaar})"
