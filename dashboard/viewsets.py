from .serializers import ReportProfileSerializer
from rest_framework import permissions,viewsets
from .d_models import ReportProfile


class ReportProfileViewSet(viewsets.ModelViewSet):
    queryset = ReportProfile.objects.all()
    serializer_class = ReportProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]