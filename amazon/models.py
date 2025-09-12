from django.db import models
from dashboard.d_models import StoreProfile, BaseCredential
from django.contrib.auth.models import User
import re

# Create your models here.

class SpapiCredential(BaseCredential):
    client_id = models.CharField(max_length=500)
    client_secret = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    """
    access_token = models.CharField(max_length=500, blank=True, null=True)
    access_token_refreshing_time = models.DateTimeField(auto_now_add=True)
    """
    
    def get_credentials(self):
        try:
            creds = {
                "refresh_token" : self.refresh_token,
                "lwa_app_id" : self.client_id,
                "lwa_client_secret" : self.client_secret
            }
            return creds
        except Exception as e:
            print(e)
            
    def are_credentials_verified(self):
        patterns = {
            "refresh_token" : r'^Atzr\|',
            "lwa_app_id" : r'^amzn1.application-oa2-client.',
            "lwa_client_secret" : r'^amzn1.oa2-cs.v1.'
        }
        credentials = self.get_credentials()
        correction_count = 0
        try:
            for credential in credentials:
                verification = re.match(
                    patterns[credential], credentials[credential]
                )
                if verification:
                    correction_count += 1
            return correction_count == len(credentials.keys())
        except Exception as e:
            print(e)
            
            
from dashboard.d_models import ReportProfile

class SpapiReportProfile(ReportProfile):
    main_section = models.CharField(max_length=20)
    sub_section = models.TextField(max_length=100)