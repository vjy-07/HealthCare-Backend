from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    """
    Represents a Doctor in the system.
    """
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

class Patient(models.Model):
    """
    Represents a Patient, created by a specific user.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # This links the Patient record to the User who created it.
    # If a User is deleted, all their patient records are also deleted.
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.age}, ({self.get_gender_display()})"

class PatientDoctorMapping(models.Model):
    """
    Maps a Patient to a Doctor, establishing a relationship.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        # Ensures that a patient can only be assigned to a specific doctor once.
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"{self.patient.name} assigned to Dr. {self.doctor.name}"
