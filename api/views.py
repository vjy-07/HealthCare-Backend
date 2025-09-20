from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
# Import the new model and serializer
from .serializers import UserSerializer, PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
from .models import Patient, Doctor, PatientDoctorMapping

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class LoginView(TokenObtainPairView):
    """
    API view for user login. Returns JWT tokens.
    """
    pass

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the patients
        for the currently authenticated user.
        """
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Assign the current user as the creator of the patient.
        """
        serializer.save(created_by=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows doctors to be viewed or edited.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

# This is the ViewSet you requested
class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for mapping patients to doctors.
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the mappings
        for the patients created by the currently authenticated user.
        """
        user = self.request.user
        # Filter mappings based on patients that belong to the current user
        return PatientDoctorMapping.objects.filter(patient__created_by=user)
