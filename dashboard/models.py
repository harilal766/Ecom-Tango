from django.db import models

# Create your models here.
class StoreProfiles(models.Model):
    storename = models.CharField(max_length=200)
    platform = models.CharField(max_length=100)
    created_date = models.CharField(max_length=200)
    
    def __str__(self):
        return self.storename
    
    def is_already_created(self):
        pass