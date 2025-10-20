from django.db import models

try:
	# Optional import to avoid circular when migrations run before scholarships exists
	from scholarships.models import Application  # type: ignore
except Exception:  # pragma: no cover - handled at runtime when app is ready
	Application = None  # type: ignore


class FinanceRecord(models.Model):
	student_name = models.CharField(max_length=200)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, choices=[
		("initiated", "Initiated"),
		("approved", "Approved"),
		("rejected", "Rejected"),
		("disbursed", "Disbursed"),
	], default="initiated")
	remarks = models.TextField(blank=True)
	# Optional FK to scholarship application (set after scholarships app is added)
	application = models.ForeignKey('scholarships.Application', null=True, blank=True, on_delete=models.SET_NULL, related_name='finance_records')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.student_name} - {self.amount} ({self.status})"

from django.db import models

# Create your models here.
