from django.db import models

# Create your models here.
class AmazonCredentials(models.Model):
    client_id = models.CharField(max_length=200)
    client_secret = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200, blank=True, null=True)
    access_token_refreshing_time = models.DateTimeField(auto_now_add=True)
    
    
    