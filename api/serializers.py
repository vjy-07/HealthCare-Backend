from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for registration.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        # We don't want to send the password back in the response.
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # The create_user method handles password hashing automatically.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Patient model.
    """
    # We want to show the username of the creator, not just the ID.
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'created_by']
        
class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Doctor model.
    """
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization']
        
class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for the PatientDoctorMapping model.
    """
    # Use ReadOnlyField with source to display names for readability
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')

    class Meta:
        model = PatientDoctorMapping
        # 'patient' and 'doctor' fields are used for writing (creating the mapping)
        # 'patient_name' and 'doctor_name' are used for reading
        fields = ['id', 'patient', 'doctor', 'patient_name', 'doctor_name']