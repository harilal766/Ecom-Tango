from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from datetime import datetime
from utils import iso_8601_timestamp

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
    main_section = models.CharField(max_length=20)
    sub_section = models.CharField(max_length=100)
    columns = models.TextField(max_length=1000)
    selected_columns = models.TextField(max_length=1000,blank=True)
    pivot_columns = models.TextField(max_length=1000, blank=True)
    tally_columns = models.TextField(max_length=1000, blank=True)
    updated_time = models.DateTimeField(auto_now_add=True,null=True)
    
    def handle_report_data(self):
        try:
            return self.columns
        except Exception as e:
            print(e)
            
    def cache_report_profiles(self, user, store):
        from amazon.views import generatable_amazon_report_types, SpapiReportClient
        from amazon.models import SpapiCredential
        report_types = {
            "Amazon" : generatable_amazon_report_types
        }
        credentials_instance = None; report_instance = None
        profile = None
        try:
            if user and store:
                for key,value in report_types[store.platform].items():
                    profile = ReportProfile.objects.filter(
                        user = user, store = store,
                        sub_section = value
                    )
                    if len(profile) == 0:
                        if store.platform == "Amazon":
                            credentials_instance = SpapiCredential(user=user, store=store)
                            report_instance = SpapiReportClient(credentials=credentials_instance.get_credentials()) 
                            id = report_instance.create_report_id(
                                reportType=value,dataStartTime=iso_8601_timestamp(0)
                            )
                            print(id)
                    
        except Exception as e:
            print(e)
            
    def create_report_profile(self,**kwargs):
        try:
            new_profile = ReportProfile.objects.create(
                user = kwargs["user"],
                store = kwargs["store"],
                main_section = kwargs["main_section"],
                sub_section = kwargs["sub_section"],
                columns = kwargs["columns"],
            )
            new_profile.save()
        except Exception as e:
            print(e)
            
            