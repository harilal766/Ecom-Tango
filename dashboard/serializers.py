from rest_framework import serializers
from dashboard.d_models import ReportProfile



class ReportProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReportProfile
        fields = '__all__'