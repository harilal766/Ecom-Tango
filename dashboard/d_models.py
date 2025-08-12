from django.db import models

# Create your models here.
class StoreProfile(models.Model):
    storename = models.CharField(max_length=200)
    platform = models.CharField(max_length=100)
    created_date = models.CharField(max_length=200)
    
    def __str__(self):
        return self.storename
    
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
    