
from django.contrib.auth.models import User
from dashboard.d_models import ReportProfile

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    current_user = serializers.SerializerMethodField()
    print(current_user)
    class Meta:
        model = User
        fields = ['id','username','url','email','groups','current_user']
        
    def get_current_user(self,obj):
        request = self.context.get('request')
        return request.user.username if request and request.user.is_authenticated else None

class ReportProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportProfile
        fields = "__all__"