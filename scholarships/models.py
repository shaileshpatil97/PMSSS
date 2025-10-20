from django.db import models
from django.utils import timezone


class Scheme(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.department})"


class Application(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("institute_verified", "Institute Verified"),
        ("department_approved", "Department Approved"),
        ("payment_initiated", "Payment Initiated"),
        ("disbursed", "Disbursed"),
        ("rejected", "Rejected"),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    applicant_name = models.CharField(max_length=200, blank=True)
    applicant_email = models.EmailField(blank=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='applications')
    institute = models.ForeignKey('institutes.Institute', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    payment_initiated_at = models.DateTimeField(null=True, blank=True)
    disbursed_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Simple helpers to transition state; viewsets will gate valid transitions
    def mark_submitted(self):
        self.status = 'submitted'
        self.submitted_at = timezone.now()

    def mark_verified(self):
        self.status = 'institute_verified'
        self.verified_at = timezone.now()

    def mark_approved(self):
        self.status = 'department_approved'
        self.approved_at = timezone.now()

    def mark_payment_initiated(self):
        self.status = 'payment_initiated'
        self.payment_initiated_at = timezone.now()

    def mark_disbursed(self):
        self.status = 'disbursed'
        self.disbursed_at = timezone.now()

    def mark_rejected(self):
        self.status = 'rejected'
        self.rejected_at = timezone.now()

    def save(self, *args, **kwargs):
        # If student provided and applicant fields empty, auto-populate
        if self.student:
            if not self.applicant_name:
                self.applicant_name = f"{self.student.first_name} {self.student.last_name}".strip()
            if not self.applicant_email:
                self.applicant_email = self.student.email
        super().save(*args, **kwargs)

    def __str__(self):
        base = self.applicant_name or (self.student and str(self.student)) or 'Applicant'
        return f"{base} - {self.scheme.name} ({self.status})"


class ApplicationDocument(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} - {self.application_id}"
from django.db import models

# Create your models here.
