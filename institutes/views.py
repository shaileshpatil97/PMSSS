from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import csv
from django.contrib.auth.decorators import login_required

from .models import Institute, InstituteVerification, InstituteStudent
from applications.models import ScholarshipApplication
from applications.models import Notification




# ===============================
# INSTITUTE DASHBOARD
# ===============================
@login_required
def institute_dashboard(request):
    if getattr(request.user, "role", None) != "INSTITUTE":
        return redirect("home")
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
@login_required
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
@login_required
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
# APPLICATIONS LIST + VERIFICATION
# ===============================
@login_required
def institute_applications(request):
    institute = Institute.objects.get(user=request.user)

    apps = ScholarshipApplication.objects.filter(
        institute_name=institute.institute_name,
        status__in=["UNDER_SCRUTINY", "SUBMITTED"],
    ).order_by("-created_at")

    verifications_by_app_id = {
        v.application_id: v
        for v in InstituteVerification.objects.filter(institute=institute, application__in=apps)
    }

    rows = [(app, verifications_by_app_id.get(app.id)) for app in apps]

    return render(request, "institute/applications.html", {
        "rows": rows,
    })


@login_required
def institute_verify_application(request, application_id):
    institute = Institute.objects.get(user=request.user)
    application = get_object_or_404(ScholarshipApplication, id=application_id)

    if application.institute_name != institute.institute_name:
        messages.error(request, "You are not allowed to verify this application.")
        return redirect("institute_applications")

    if request.method == "POST":
        action = request.POST.get("action")
        remarks = (request.POST.get("remarks") or "").strip()

        verification, _ = InstituteVerification.objects.get_or_create(
            application=application,
            institute=institute,
        )

        if action == "verify":
            verification.status = "VERIFIED"
            verification.remarks = remarks
            verification.save(update_fields=["status", "remarks", "verified_at"])
            application.status = "APPROVED"
            application.save(update_fields=["status"])
            Notification.objects.create(
                student=application.student,
                message=f"Institute verified your application. {('Remarks: ' + remarks) if remarks else ''}",
            )
            messages.success(request, "Application verified.")
        elif action == "reject":
            verification.status = "REJECTED"
            verification.remarks = remarks
            verification.save(update_fields=["status", "remarks", "verified_at"])
            application.status = "REJECTED"
            application.save(update_fields=["status"])
            Notification.objects.create(
                student=application.student,
                message=f"Institute rejected your application. {('Remarks: ' + remarks) if remarks else ''}",
            )
            messages.success(request, "Application rejected.")
        else:
            messages.error(request, "Invalid action.")

        return redirect("institute_applications")

    verification = InstituteVerification.objects.filter(application=application, institute=institute).first()
    return render(request, "institute/verify_application.html", {
        "app": application,
        "verification": verification,
    })
