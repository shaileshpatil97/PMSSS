from django.http import JsonResponse
from .models import AppliSarkarRecord

def verify_student(request, aadhaar):
    try:
        rec = AppliSarkarRecord.objects.get(aadhaar=aadhaar)
        return JsonResponse({
            "aadhaar": rec.aadhaar,
            "domicile": rec.domicile_state,
            "fraud": rec.is_fraud,
            "previous_scholarship": rec.previous_scholarship
        })
    except AppliSarkarRecord.DoesNotExist:
        return JsonResponse({"error": "No record"}, status=404)
