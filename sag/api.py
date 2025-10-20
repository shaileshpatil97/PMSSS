from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from .models import SAG
from .serializers import SAGSerializer


class SAGViewSet(viewsets.ModelViewSet):
    queryset = SAG.objects.all().order_by('-id')
    serializer_class = SAGSerializer
    filterset_fields = ["name"]


router = DefaultRouter()
router.register(r'sag', SAGViewSet, basename='sag')
