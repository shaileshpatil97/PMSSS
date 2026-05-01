from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import identify_hasher

from applications.models import ScholarshipApplication, ScholarshipScheme, Notification

from .forms import LoginForm, StudentRegistrationForm
from .models import StudentProfile, User


def _authenticate_aadhaar_password(request, aadhaar: str, password: str):
    """Authenticate using Aadhaar+password.

    Also supports a one-time upgrade of legacy plaintext passwords that may exist
    in the DB (i.e., `user.password` is not a valid Django-encoded hash).
    """

    if not aadhaar or not password:
        return None

    # Prefer the standard keyword, but keep backward compatibility.
    user = authenticate(request, username=aadhaar, password=password)
    if user is None:
        user = authenticate(request, aadhaar=aadhaar, password=password)
    if user is not None:
        return user

    candidate = User.objects.filter(aadhaar=aadhaar).first()
    if candidate is None or not getattr(candidate, "is_active", True):
        return None

    # If the stored password isn't a valid encoded hash, and it matches the
    # submitted password, upgrade it to a proper hash.
    try:
        identify_hasher(candidate.password)
        return None
    except ValueError:
        if candidate.password == password:
            candidate.set_password(password)
            candidate.save(update_fields=["password"])
            return authenticate(request, username=aadhaar, password=password)

    return None


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                aadhaar=form.cleaned_data['aadhaar'],
                password=form.cleaned_data['password'],
                role="STUDENT"
            )
            profile, _ = StudentProfile.objects.get_or_create(student=user)
            profile.full_name = form.cleaned_data['full_name']
            profile.dob = form.cleaned_data['dob']
            profile.mobile = form.cleaned_data['mobile']
            profile.email = form.cleaned_data['email']
            profile.address = form.cleaned_data['address']
            profile.save()
            return redirect("home")
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            aadhaar = form.cleaned_data.get("aadhaar")
            password = form.cleaned_data.get("password")

            user = _authenticate_aadhaar_password(request, aadhaar=aadhaar, password=password)

            if user is not None:
                login(request, user)

                if user.role == "STUDENT":
                    return redirect("student_home")

                elif user.role == "INSTITUTE":
                    return redirect("/institute/dashboard/")

                elif user.role == "ADMIN":
                    return redirect("/admin/")

            else:
                error = "Invalid Aadhaar or Password"
    else:
        form = LoginForm()

    return render(request, "login.html", {
        "form": form,
        "error": error
    })


def institute_login_view(request):
    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            aadhaar = form.cleaned_data.get("aadhaar")
            password = form.cleaned_data.get("password")

            user = _authenticate_aadhaar_password(request, aadhaar=aadhaar, password=password)

            if user is not None and user.role == "INSTITUTE":
                login(request, user)
                return redirect("institute_dashboard")

            error = "Invalid Institute Aadhaar or Password"
    else:
        form = LoginForm()

    return render(request, "institute_login.html", {
        "form": form,
        "error": error,
    })


@login_required
def profile_personal(request):
    profile, _ = StudentProfile.objects.get_or_create(student=request.user)

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name")
        profile.dob = request.POST.get("dob")
        profile.gender = request.POST.get("gender")
        profile.mobile = request.POST.get("mobile")
        profile.email = request.POST.get("email")
        profile.save()
        return redirect("profile_address")

    return render(request, "profile/personal.html", {"profile": profile})


@login_required
def profile_address(request):
    profile = StudentProfile.objects.get(student=request.user)

    if request.method == "POST":
        profile.address = request.POST.get("address")
        profile.district = request.POST.get("district")
        profile.state = request.POST.get("state")
        profile.pincode = request.POST.get("pincode")
        profile.save()
        return redirect("profile_other")

    return render(request, "profile/address.html", {"profile": profile})


@login_required
def profile_other(request):
    profile = StudentProfile.objects.get(student=request.user)
    if request.method == "POST":
        profile.caste = request.POST.get("caste")
        income = request.POST.get("income")
        profile.income = int(income) if income else None         
        profile.save()
        return redirect("profile_course")
    return render(request, "profile/other.html", {"profile": profile})

@login_required
def profile_course(request):
    profile = StudentProfile.objects.get(student=request.user)
    if request.method == "POST":
        profile.course = request.POST.get("course")
        profile.institute = request.POST.get("institute")
        profile.year = request.POST.get("year")
        profile.save()
        return redirect("profile_qualification")
    return render(request, "profile/course.html", {"profile": profile})

@login_required
def profile_qualification(request):
    profile = StudentProfile.objects.get(student=request.user)
    if request.method == "POST":
        profile.last_qualification = request.POST.get("last_qualification")
        profile.save()
        return redirect("profile_hostel")
    return render(request, "profile/qualification.html", {"profile": profile})

@login_required
def profile_hostel(request):
    profile = StudentProfile.objects.get(student=request.user)
    if request.method == "POST":
        profile.hostel = True if request.POST.get("hostel") else False
        profile.save()
        return redirect("profile_documents")
    return render(request, "profile/hostel.html", {"profile": profile})

@login_required
def profile_documents(request):
    profile = StudentProfile.objects.get(student=request.user)
    if request.method == "POST":
        profile.caste_cert_no = request.POST.get("caste_cert_no")
        profile.caste_validity_cert_no = request.POST.get("caste_validity_cert_no")
        profile.ncl_cert_no = request.POST.get("ncl_cert_no")
        profile.domicile_cert_no = request.POST.get("domicile_cert_no")
        profile.income_cert_no = request.POST.get("income_cert_no")

        if "caste_cert" in request.FILES:
            profile.caste_cert = request.FILES["caste_cert"]
        if "caste_validity_cert" in request.FILES:
            profile.caste_validity_cert = request.FILES["caste_validity_cert"]
        if "ncl_cert" in request.FILES:
            profile.ncl_cert = request.FILES["ncl_cert"]
        if "domicile_cert" in request.FILES:
            profile.domicile_cert = request.FILES["domicile_cert"]
        if "income_cert" in request.FILES:
            profile.income_cert = request.FILES["income_cert"]
            
        profile.save()
        return redirect("student_home")
    return render(request, "profile/documents.html", {"profile": profile})

@login_required
def student_home(request):
    profile = getattr(request.user, "studentprofile", None)
    completeness_percentage = 0
    if profile:
        fields_to_check = [
            profile.full_name, profile.dob, profile.gender, profile.mobile,
            profile.email, profile.address, profile.district, profile.state,
            profile.pincode, profile.caste, profile.income, profile.course,
            profile.institute, profile.year, profile.last_qualification,
            profile.caste_cert, profile.caste_cert_no,
            profile.caste_validity_cert, profile.caste_validity_cert_no,
            profile.ncl_cert, profile.ncl_cert_no,
            profile.domicile_cert, profile.domicile_cert_no,
            profile.income_cert, profile.income_cert_no
        ]
        filled_fields = sum(1 for field in fields_to_check if field is not None and field != "")
        total_fields = len(fields_to_check)
        completeness_percentage = int((filled_fields / total_fields) * 100)

    return render(request, "student_home.html", {"completeness_percentage": completeness_percentage})

@login_required
def my_applied(request):
    apps = ScholarshipApplication.objects.filter(
        student=request.user,
        status__in=["SUBMITTED","UNDER_SCRUTINY","APPROVED"]
    )
    return render(request,"my_applied.html",{"apps":apps})

@login_required
def my_cancelled(request):
    apps = ScholarshipApplication.objects.filter(student=request.user, status="CANCELLED")
    return render(request, "my_cancelled.html", {"apps": apps})

@login_required
def scheme_history(request):
    apps = ScholarshipApplication.objects.filter(student=request.user)
    return render(request,"scheme_history.html",{"apps":apps})


@login_required
def notifications(request):
    notes = Notification.objects.filter(student=request.user)
    return render(request,"notifications.html",{"notes":notes})


@login_required
def all_schemes(request):
    profile = StudentProfile.objects.filter(student=request.user).first()
    if profile is None:
        return redirect("profile_personal")

    # If the student hasn't completed the profile yet, avoid filtering with None.
    if profile.income is None or not profile.caste:
        schemes = ScholarshipScheme.objects.none()
    else:
        schemes = ScholarshipScheme.objects.filter(
            caste=profile.caste,
        )

    return render(request, "schemes.html", {"schemes": schemes})

