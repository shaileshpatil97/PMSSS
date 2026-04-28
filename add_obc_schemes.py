import os
import django

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmsss_core.settings')
    django.setup()

    from applications.models import ScholarshipScheme

    obc_schemes = [
        "Post Matric Scholarship to OBC Students",
        "Tuition Fees and Examination Fees to OBC Students",
        "Post Matric Scholarship for OBC Girls in Professional Courses",
        "Tuition Fee and Examination Fee for OBC Girls Pursuing Professional Courses",
        "Vocational Training Fee Reimbursement for OBC Student"
    ]

    for name in obc_schemes:
        # Use 'computer' as the default course since the test user is using 'computer'
        ScholarshipScheme.objects.get_or_create(
            name=name,
            defaults={
                'department': 'OBC Welfare Department',
                'min_income': 0, # so it matches any income
                'caste': 'OBC',
                'course': 'computer' 
            }
        )

    print("OBC Schemes added successfully!")

if __name__ == '__main__':
    main()
