from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()


router.register(r'users',UserViewSet)

urlpatterns = [
    path('router/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


