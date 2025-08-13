from django.db import models
from dashboard.d_models import StoreProfile, BaseCredential
from django.contrib.auth.models import User

# Create your models here.


class SpapiCredential(BaseCredential):
    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200, blank=True, null=True)
    access_token_refreshing_time = models.DateTimeField(auto_now_add=True)