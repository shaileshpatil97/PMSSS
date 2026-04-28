from django.contrib import admin
from .models import Institute, InstituteVerification
from .models import InstituteStudent

admin.site.register(Institute)
admin.site.register(InstituteVerification)
admin.site.register(InstituteStudent)