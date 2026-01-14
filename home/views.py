from django.shortcuts import render
from applications.models import ScholarshipApplication

def home(request):
    return render(request, "home.html")


def student_home(request):
    total = ScholarshipApplication.objects.filter(student=request.user).count()
    approved = ScholarshipApplication.objects.filter(student=request.user, status="APPROVED").count()
    rejected = ScholarshipApplication.objects.filter(student=request.user, status="REJECTED").count()

    return render(request, "student_home.html", {
        "total": total,
        "approved": approved,
        "rejected": rejected
    })
