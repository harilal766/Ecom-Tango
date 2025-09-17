from django.contrib.auth.models import User
from dashboard.d_models import ReportProfile, StoreProfile
from rest_framework import permissions,viewsets

from .serializers import UserSerializer, ReportProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReportProfileViewSet(viewsets.ModelViewSet):
    queryset = ReportProfile.objects.all() 
    serializer_class = ReportProfileSerializer
    #permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user = self.request.user 
        store = StoreProfile.objects.get(user = user)
        return ReportProfile.objects.filter(
            user = user, store = store
        )