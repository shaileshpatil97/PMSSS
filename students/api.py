from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-id')
    serializer_class = StudentSerializer
    filterset_fields = ["first_name", "last_name", "email"]


router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
