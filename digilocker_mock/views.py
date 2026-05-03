from django.http import JsonResponse
from .models import DigiLockerRecord

def fetch_docs(request, aadhaar):
    try:
        rec = DigiLockerRecord.objects.get(aadhaar=aadhaar)
        return JsonResponse({
            "aadhaar": rec.aadhaar,
            "income": rec.income_certificate_no,
            "caste": rec.caste_certificate_no,
            "domicile": rec.domicile_certificate_no,
            "non_creamy_layer": rec.non_creamy_layer_certificate_no,
        })
    except DigiLockerRecord.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)
