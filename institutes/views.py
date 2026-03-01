from django.shortcuts import render, redirect
from django.contrib import messages
import csv

from .models import Institute, InstituteVerification, InstituteStudent
from applications.models import ScholarshipApplication




# ===============================
# INSTITUTE DASHBOARD
# ===============================
def institute_dashboard(request):
    institute = Institute.objects.get(user=request.user)

    total_students = ScholarshipApplication.objects.filter(
        institute_name=institute.institute_name
    ).count()

    submitted = ScholarshipApplication.objects.filter(
        institute_name=institute.institute_name,
        status="SUBMITTED"
    ).count()

    pending = InstituteVerification.objects.filter(
        institute=institute,
        status="PENDING"
    ).count()

    verified = InstituteVerification.objects.filter(
        institute=institute,
        status="VERIFIED"
    ).count()

    rejected = InstituteVerification.objects.filter(
        institute=institute,
        status="REJECTED"
    ).count()

    return render(request, "institute/dashboard.html", {
        "total_students": total_students,
        "submitted": submitted,
        "pending": pending,
        "verified": verified,
        "rejected": rejected,
    })



# ===============================
# CSV UPLOAD
# ===============================
def upload_students_csv(request):
    try:
        institute = Institute.objects.get(user=request.user)
    except Institute.DoesNotExist:
        messages.error(
            request,
            "Institute profile not found. Please complete institute registration first."
        )
        return redirect("institute_dashboard")

    if request.method == "POST" and request.FILES.get("file"):
        csv_file = request.FILES["file"]
        decoded = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded)

        for row in reader:
            InstituteStudent.objects.get_or_create(
                institute=institute,
                aadhaar=row["aadhaar"],
                defaults={
                    "student_name": row["student_name"],
                    "course": row["course"],
                    "year": row["year"],
                }
            )

        messages.success(request, "Students uploaded successfully.")
        return redirect("institute_dashboard")

    return render(request, "institute/upload_students.html")


# ===============================
# FILLED vs NOT FILLED
# ===============================
def institute_student_tracking(request):
    institute = Institute.objects.get(user=request.user)

    applied_aadhaars = ScholarshipApplication.objects.filter(
        institute_name=institute.institute_name
    ).values_list("student__aadhaar", flat=True)

    filled_students = InstituteStudent.objects.filter(
        institute=institute,
        aadhaar__in=applied_aadhaars
    )

    not_filled_students = InstituteStudent.objects.filter(
        institute=institute
    ).exclude(
        aadhaar__in=applied_aadhaars
    )

    return render(request, "institute/student_tracking.html", {
        "filled_students": filled_students,
        "not_filled_students": not_filled_students,
    })


# ===============================
# REJECTED APPLICATIONS
# ===============================
def rejected_applications(request):
    institute = Institute.objects.get(user=request.user)

    rejected_apps = ScholarshipApplication.objects.filter(
        institute_name=institute.institute_name,
        status="REJECTED"
    )

    return render(request, "institute/rejected_applications.html", {
        "rejected_apps": rejected_apps
    })
