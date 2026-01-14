from django.shortcuts import render, redirect
from .forms import ApplicationForm
from .models import ScholarshipApplication
from .verification import auto_verify
from .models import ApplicationDocuments


def new_application(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.student = request.user
            app.status = "SUBMITTED"
            app.save()
            return redirect("dashboard")
    else:
        form = ApplicationForm()
    return render(request, "new_application.html", {"form": form})





def student_dashboard(request):
    apps = ScholarshipApplication.objects.filter(student=request.user)
    return render(request, "student_dashboard.html", {"apps": apps})

