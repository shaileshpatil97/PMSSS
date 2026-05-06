from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import csv
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
import re

from .models import Institute, InstituteVerification, InstituteStudent
from applications.models import ScholarshipApplication
from applications.models import Notification


def _normalize_csv_key(key: str) -> str:
    return (key or "").strip().lower().replace(" ", "").replace("_", "")


def _parse_year(raw_value):
    value = str(raw_value or "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return int(Decimal(value))
        except (InvalidOperation, ValueError):
            return None


def _parse_aadhaar(raw_value):
    value = str(raw_value or "").strip().replace("\ufeff", "")
    if not value:
        return None

    digits = ""
    if value.isdigit():
        digits = value
    else:
        try:
            d = Decimal(value)
            # Convert things like 4.56985E+11 to a full integer string
            if d == d.to_integral_value():
                digits = format(d, "f")
            else:
                digits = value
        except InvalidOperation:
            digits = value

    digits = re.sub(r"\D", "", digits)
    if not digits:
        return None

    if len(digits) < 12:
        digits = digits.zfill(12)

    if len(digits) != 12:
        # Avoid truncating; better to skip and let the institute fix CSV.
        return None

    return digits


def _get_institute_or_redirect(request):
    if getattr(request.user, "role", None) != "INSTITUTE":
        return None, redirect("home")

    institute = Institute.objects.filter(user=request.user).first()
    if institute is None:
        institute = Institute.objects.create(
            user=request.user,
            institute_code=f"INST-{request.user.aadhaar}",
            institute_name="SSBT COET",
            address="Pending Update",
            district="Pending Update",
            state="Pending Update",
            contact_email="institute@example.com",
            contact_phone="0000000000"
        )
        messages.info(request, "Institute profile auto-created. Please update your details in the admin panel.")

    return institute, None




# ===============================
# INSTITUTE DASHBOARD
# ===============================
@login_required
def institute_dashboard(request):
    institute, redirect_response = _get_institute_or_redirect(request)
    if redirect_response:
        return redirect_response

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
    institute, redirect_response = _get_institute_or_redirect(request)
    if redirect_response:
        return redirect_response

    if request.method == "POST" and request.FILES.get("file"):
        csv_file = request.FILES["file"]
        decoded_lines = csv_file.read().decode("utf-8-sig", errors="replace").splitlines()

        # Some exports end up "double-encoded" where each row is a single quoted column
        # that itself contains a comma-separated line (e.g. "aadhaar,student_name,...").
        # Detect and normalize that into proper CSV lines.
        preview_rows = list(csv.reader(decoded_lines[:5]))
        if preview_rows and all(len(r) == 1 for r in preview_rows) and any("," in r[0] for r in preview_rows):
            decoded_lines = [r[0] for r in csv.reader(decoded_lines)]

        reader = csv.DictReader(decoded_lines)

        created_count = 0
        updated_count = 0
        skipped_count = 0
        duplicate_in_file_count = 0
        seen_aadhaars = set()

        for row in reader:
            normalized_row = {
                _normalize_csv_key(k): (v.strip() if isinstance(v, str) else v)
                for k, v in (row or {}).items()
            }

            aadhaar = _parse_aadhaar(
                normalized_row.get("aadhaar")
                or normalized_row.get("aadhar")
            )
            student_name = (
                normalized_row.get("studentname")
                or normalized_row.get("name")
                or normalized_row.get("student")
                or ""
            ).strip()
            course = (normalized_row.get("course") or "").strip()
            year = _parse_year(normalized_row.get("year") or normalized_row.get("class"))

            if not aadhaar or not student_name or not course or year is None:
                skipped_count += 1
                continue

            if aadhaar in seen_aadhaars:
                duplicate_in_file_count += 1
                continue
            seen_aadhaars.add(aadhaar)

            _, was_created = InstituteStudent.objects.update_or_create(
                institute=institute,
                aadhaar=aadhaar,
                defaults={
                    "student_name": student_name,
                    "course": course,
                    "year": year,
                },
            )
            if was_created:
                created_count += 1
            else:
                updated_count += 1

        if created_count or updated_count:
            messages.success(
                request,
                f"Upload complete. Created {created_count}, updated {updated_count}."
            )
        if duplicate_in_file_count:
            messages.warning(
                request,
                f"Skipped {duplicate_in_file_count} duplicate Aadhaar rows in the CSV file."
            )
        if skipped_count:
            messages.warning(
                request,
                f"Skipped {skipped_count} rows due to missing/invalid Aadhaar, name, course, or year."
            )

        return redirect("institute_student_tracking")

    return render(request, "institute/upload_students.html")


# ===============================
# FILLED vs NOT FILLED
# ===============================
@login_required
def institute_student_tracking(request):
    institute, redirect_response = _get_institute_or_redirect(request)
    if redirect_response:
        return redirect_response

    applied_aadhaars = ScholarshipApplication.objects.filter(
        institute_name=institute.institute_name
    ).values_list("student__aadhaar", flat=True).distinct()

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
    institute, redirect_response = _get_institute_or_redirect(request)
    if redirect_response:
        return redirect_response

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
    institute, redirect_response = _get_institute_or_redirect(request)
    if redirect_response:
        return redirect_response
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
