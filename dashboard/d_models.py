from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StoreProfile(models.Model):
    slug = models.SlugField(default="",null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    platform = models.CharField(max_length=30)
    storename = models.CharField(max_length=200)
    created_date = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.storename} : {self.platform}"
    
    def is_already_created(self,storename):
        try:
            added_stores = StoreProfile.objects.all()
            added_stores = [store.storename for store in added_stores]
            if storename in added_stores:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            

class BaseCredential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(StoreProfile,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.store.storename
    