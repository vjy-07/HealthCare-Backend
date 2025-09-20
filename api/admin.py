from django.contrib import admin
from .models import Doctor, Patient, PatientDoctorMapping

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(PatientDoctorMapping)
