import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, aadhaar, password=None, role="STUDENT"):
        if not aadhaar:
            raise ValueError("Aadhaar is required")
        user = self.model(aadhaar=aadhaar, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, aadhaar, password):
        user = self.create_user(aadhaar, password, role="ADMIN")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("STUDENT", "Student"),
        ("INSTITUTE", "Institute"),
        ("OFFICER", "Officer"),
        ("ADMIN", "Admin"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aadhaar = models.CharField(max_length=12, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "aadhaar"


# THIS MUST BE A SEPARATE MODEL (not inside User)

class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)
    mobile = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)

    address = models.TextField(null=True)
    district = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=6, null=True)

    caste = models.CharField(max_length=30, null=True)
    income = models.IntegerField(null=True)

    course = models.CharField(max_length=50, null=True)
    institute = models.CharField(max_length=100, null=True)
    year = models.IntegerField(null=True)

    last_qualification = models.CharField(max_length=100, null=True)
    hostel = models.BooleanField(default=False)

    # Documents
    caste_cert_no = models.CharField(max_length=50, null=True, blank=True)
    caste_cert = models.FileField(upload_to="documents/", null=True, blank=True)

    caste_validity_cert_no = models.CharField(max_length=50, null=True, blank=True)
    caste_validity_cert = models.FileField(upload_to="documents/", null=True, blank=True)

    ncl_cert_no = models.CharField(max_length=50, null=True, blank=True)
    ncl_cert = models.FileField(upload_to="documents/", null=True, blank=True)

    domicile_cert_no = models.CharField(max_length=50, null=True, blank=True)
    domicile_cert = models.FileField(upload_to="documents/", null=True, blank=True)

    income_cert_no = models.CharField(max_length=50, null=True, blank=True)
    income_cert = models.FileField(upload_to="documents/", null=True, blank=True)
