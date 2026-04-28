import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmsss_core.settings')
django.setup()

from applications.models import ScholarshipScheme

sc_schemes = [
    "Government of India Post-Matric Scholarship",
    "Post-Matric Tuition Fee and Examination Fee (Freeship)",
    "Maintenance Allowance for Student's Studying in Professional Courses",
    "Rajarshri Chhatrapati Shahu Maharaj Merit Scholarship",
    "Post-Matric Scholarship for Persons with Disability",
    "Vocational Training Fee Reimbursement for Students belonging to Scheduled Caste Category",
    "Swadhar Yojana (Hostel Maintenance Allowance)",
    "Dr. Babasaheb Ambedkar Swadhar Yojana"
]

for name in sc_schemes:
    ScholarshipScheme.objects.get_or_create(
        name=name,
        defaults={
            'department': 'Social Justice and Special Assistance',
            'min_income': 0,
            'caste': 'SC',
            'course': 'computer' 
        }
    )

print("SC Schemes added successfully!")
