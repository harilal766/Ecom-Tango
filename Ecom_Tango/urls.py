"""
URL configuration for Ecom_Tango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

<<<<<<< HEAD
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
        
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
=======


>>>>>>> e7821f5eb815f88c8a36995c66a3bc5e2cecd1e4
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('dashboard.d_urls')),
    path('auth/',include('authorization.auth_urls')),
    #path('amazon/',include('amazon.a_urls')),
    #path('shopify/',include('shopify.urls')),
<<<<<<< HEAD
    path('api-auth/',include('rest_framework.urls')),
    
    path('router/',include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
=======
    
    # drf
    path('api/',include('api.urls'))
>>>>>>> e7821f5eb815f88c8a36995c66a3bc5e2cecd1e4
]
