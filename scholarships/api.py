from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from django.db import transaction
from django.shortcuts import redirect
from decimal import Decimal, InvalidOperation
from .models import Scheme, Application
from .serializers import SchemeSerializer, ApplicationSerializer
from finance.models import FinanceRecord


class SchemeViewSet(viewsets.ModelViewSet):
    queryset = Scheme.objects.all().order_by('name')
    serializer_class = SchemeSerializer
    filterset_fields = ["department", "is_active", "name"]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-id')
    serializer_class = ApplicationSerializer
    filterset_fields = ["status", "scheme", "applicant_email", "institute"]

    def _invalid_transition(self, current: str, target: str) -> Response:
        return Response({"detail": f"Invalid transition from {current} to {target}"}, status=status.HTTP_400_BAD_REQUEST)

    def _maybe_redirect(self, request, app):
        # If request comes from an HTML form, redirect back to detail page
        accept = request.META.get('HTTP_ACCEPT', '')
        if 'text/html' in accept:
            return redirect(f'/scholarships/applications/{app.pk}/')
        return Response(self.get_serializer(app).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def submit(self, request, pk=None):
        app = self.get_object()
        if app.status != 'draft':
            return self._invalid_transition(app.status, 'submitted')
        app.mark_submitted()
        app.save()
        return self._maybe_redirect(request, app)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def verify_institute(self, request, pk=None):
        if not (request.user.is_staff or request.user.groups.filter(name='Institute').exists()):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        app = self.get_object()
        if app.status != 'submitted':
            return self._invalid_transition(app.status, 'institute_verified')
        app.mark_verified()
        app.save()
        return self._maybe_redirect(request, app)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def approve_department(self, request, pk=None):
        if not (request.user.is_staff or request.user.groups.filter(name='Department').exists()):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        app = self.get_object()
        if app.status != 'institute_verified':
            return self._invalid_transition(app.status, 'department_approved')
        app.mark_approved()
        app.save()
        return self._maybe_redirect(request, app)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def initiate_payment(self, request, pk=None):
        if not (request.user.is_staff or request.user.groups.filter(name='Department').exists()):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        app = self.get_object()
        if app.status != 'department_approved':
            return self._invalid_transition(app.status, 'payment_initiated')
        app.mark_payment_initiated()
        app.save()
        # Create a finance record placeholder
        raw_amount = request.data.get('amount', 0)
        try:
            amount = Decimal(str(raw_amount or 0))
        except (InvalidOperation, TypeError):
            amount = Decimal('0')
        FinanceRecord.objects.create(
            student_name=app.applicant_name,
            amount=amount or 0,
            status='initiated',
            remarks=f"Auto-created for application {app.id}",
            application=app,
        )
        return self._maybe_redirect(request, app)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def disburse(self, request, pk=None):
        if not (request.user.is_staff or request.user.groups.filter(name='Finance').exists()):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        app = self.get_object()
        if app.status not in ('payment_initiated', 'department_approved'):
            return self._invalid_transition(app.status, 'disbursed')
        app.mark_disbursed()
        app.save()
        # Update finance records
        app.finance_records.update(status='disbursed')
        return self._maybe_redirect(request, app)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        if not (request.user.is_staff or request.user.groups.filter(name__in=['Institute','Department','Finance']).exists()):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        app = self.get_object()
        if app.status in ('disbursed',):
            return self._invalid_transition(app.status, 'rejected')
        app.mark_rejected()
        app.save()
        app.finance_records.update(status='rejected')
        return self._maybe_redirect(request, app)


router = DefaultRouter()
router.register(r'schemes', SchemeViewSet, basename='scheme')
router.register(r'applications', ApplicationViewSet, basename='application')
