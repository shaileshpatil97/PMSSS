from django.db import models


class Institute(models.Model):
	ADMISSION_CHOICES = [
		("pending", "Pending"),
		("admitted", "Admitted"),
		("rejected", "Rejected"),
	]
	ESUVIDHA_CHOICES = [
		("not_applied", "Not Applied"),
		("applied", "Applied"),
		("approved", "Approved"),
		("rejected", "Rejected"),
	]

	name = models.CharField(max_length=200)
	code = models.CharField(max_length=50, unique=True)
	address = models.TextField(blank=True)
	admission_status = models.CharField(max_length=20, choices=ADMISSION_CHOICES, default="pending")
	esuvidha_status = models.CharField(max_length=20, choices=ESUVIDHA_CHOICES, default="not_applied")
	contact_email = models.EmailField(blank=True)
	contact_phone = models.CharField(max_length=20, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.code} - {self.name}"

from django.db import models

# Create your models here.
