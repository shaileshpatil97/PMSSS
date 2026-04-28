import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmsss_core.settings')
django.setup()

from applications.models import ScholarshipScheme

general_schemes = [
    "Rajarshi Chhatrapati Shahu Maharaj Shikshan Shulkh Shishyavrutti Yojna (EBC)",
    "Dr Panjabrao Deshmukh Vastigruh Nirvah Bhatta Yojna (DTE)",
    "Dr Panjabrao Deshmukh Hostel Maintenance Allowance",
    "Rajarshri Chhatrapati Shahu Maharaj Fee Reimbursement Scheme",
    "Education Fee Reimbursement for Open Category Students affected due to SEBC and EWS Reservation in Medical and Dental Colleges",
    "Reimbursement of Tuition Fee and Examination Fee for Girls under Rajarshri Chhatrapati Shahu Maharaj Tuition Fee Scholarship Scheme",
    "Vocational Training Fee Reimbursement for Open Category (Economically Weaker Section) Students",
    "State Government Open Merit Scholarship",
    "Eklavya Scholarship",
    "Assistance to Meritorious Students Scholarship (Junior Level)",
    "Assistance to Meritorious Students Scholarship (Senior Level)",
    "Government Vidyaniketan Scholarship",
    "State Government Dakshina Adhichatra Scholarship"
]

for name in general_schemes:
    ScholarshipScheme.objects.get_or_create(
        name=name,
        defaults={
            'department': 'Higher and Technical Education',
            'min_income': 0,
            'caste': 'General',
            'course': 'computer' 
        }
    )

print("General Schemes added successfully!")
