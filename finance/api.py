from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from .models import FinanceRecord
from .serializers import FinanceRecordSerializer


class FinanceRecordViewSet(viewsets.ModelViewSet):
    queryset = FinanceRecord.objects.all().order_by('-id')
    serializer_class = FinanceRecordSerializer
    filterset_fields = ["student_name", "status"]


router = DefaultRouter()
router.register(r'finance-records', FinanceRecordViewSet, basename='finance-record')
