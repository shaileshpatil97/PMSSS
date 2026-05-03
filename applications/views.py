from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from .models import ScholarshipApplication
from .verification import auto_verify
from .models import ApplicationDocuments
from .models import Notification


@login_required
def new_application(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.student = request.user
            app.status = "SUBMITTED"
            app.save()

            verified, payload = auto_verify(app, request.user.aadhaar)
            if verified:
                ApplicationDocuments.objects.update_or_create(
                    application=app,
                    defaults={
                        "income_cert": payload.get("income", ""),
                        "caste_cert": payload.get("caste", ""),
                        "domicile_cert": payload.get("domicile", ""),
                        "non_creamy_layer_cert": payload.get("non_creamy_layer", ""),
                        "verified": True,
                    },
                )
                app.status = "UNDER_SCRUTINY"
                app.save(update_fields=["status"])
                Notification.objects.create(
                    student=request.user,
                    message="Application submitted and documents auto-verified. Awaiting institute scrutiny.",
                )
            else:
                app.status = "REJECTED"
                app.save(update_fields=["status"])
                Notification.objects.create(
                    student=request.user,
                    message=f"Application auto-verification failed: {payload}",
                )
            return redirect("dashboard")
    else:
        form = ApplicationForm()
    return render(request, "new_application.html", {"form": form})





@login_required
def student_dashboard(request):
    apps = ScholarshipApplication.objects.filter(student=request.user)
    return render(request, "student_dashboard.html", {"apps": apps})

