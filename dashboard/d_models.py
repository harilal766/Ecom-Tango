from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class StoreProfile(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    storename = models.CharField(max_length=200)
    platform = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.storename} : {self.platform}"
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.storename)
        super(StoreProfile,self).save(*args,**kwargs)

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
        return f"{self.store}"
    
    @classmethod
    def get_credentials(cls,user, store_slug):
        credentials = None
        try:
            selected_store = StoreProfile.objects.get(
                user = user, slug=store_slug
            )
            credentials = cls.objects.get(
                user=user, store = selected_store
            )
        except Exception as e:
            print(e)
        finally:
            return credentials
    
from datetime import datetime
class ReportProfile(BaseCredential):
    columns = models.TextField(max_length=1000)
    selected_columns = models.TextField(max_length=1000,blank=True)
    main_section = models.CharField(max_length=20)
    sub_section = models.CharField(max_length=100)
    updated_time = models.DateTimeField(auto_now_add=True,null=True)
    
    def handle_report_data(self):
        try:
            return self.columns
        except Exception as e:
            print(e)
            
    def cache_report_columns(self,selected_columns : str = None):
        try:
            if selected_columns:
                self.selected_columns = ','.join(selected_columns) 
                self.save()
        except Exception as e:
            print(e)