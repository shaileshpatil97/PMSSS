from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from .models import User, StudentProfile
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .models import StudentProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from applications.models import ScholarshipApplication , ScholarshipScheme , Notification


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                aadhaar=form.cleaned_data['aadhaar'],
                password=form.cleaned_data['password'],
                role="STUDENT"
            )
            StudentProfile.objects.create(
                student=user,
                full_name=form.cleaned_data['full_name'],
                dob=form.cleaned_data['dob'],
                mobile=form.cleaned_data['mobile'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address']
            )
            return redirect("home")
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                aadhaar=form.cleaned_data['aadhaar'],
                password=form.cleaned_data['password']
            )
            if user and user.role == "STUDENT":
                login(request, user)
                return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


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
        return redirect("student_home")
    return render(request, "profile/hostel.html", {"profile": profile})

@login_required
def student_home(request):
    return render(request, "student_home.html")

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
    profile = StudentProfile.objects.get(student=request.user)

    schemes = ScholarshipScheme.objects.filter(
        min_income__lte = profile.income,
        caste = profile.caste,
        course = profile.course
    )

    return render(request, "schemes.html", {"schemes": schemes})

