
from django.contrib.auth.models import User
from dashboard.d_models import ReportProfile

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username','url','email','groups']


class ReportProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportProfile
        fields = ["user","store","columns"]