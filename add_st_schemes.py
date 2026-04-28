import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmsss_core.settings')
django.setup()

from applications.models import ScholarshipScheme

st_schemes = [
    "Government of India Post-Matric Scholarship (ST Students)",
    "Tuition Fee & Examination Fee (Freeship) – ST Category",
    "Vocational Education Fee Reimbursement – ST Students",
    "Vocational Education Maintenance Allowance – ST Students",
    "Post Matric Scholarship Scheme (Government Of India)",
    "Tuition Fee & Exam Fee for Tribal Students (Freeship)"
]

for name in st_schemes:
    ScholarshipScheme.objects.get_or_create(
        name=name,
        defaults={
            'department': 'Tribal Development Department',
            'min_income': 0,
            'caste': 'ST',
            'course': 'computer' 
        }
    )

print("ST Schemes added successfully!")
