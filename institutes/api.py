from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from .models import Institute
from .serializers import InstituteSerializer


class InstituteViewSet(viewsets.ModelViewSet):
    queryset = Institute.objects.all().order_by('-id')
    serializer_class = InstituteSerializer
    filterset_fields = ["code", "name", "admission_status", "esuvidha_status"]


router = DefaultRouter()
router.register(r'institutes', InstituteViewSet, basename='institute')
