from django.db import models
from dashboard.d_models import BaseCredential

# Create your models here.
class ShopifyApiCredential(BaseCredential):
    storename = models.CharField(max_length=10)
    access_token = models.CharField(max_length=200)