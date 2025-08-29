from django.test import TestCase

from authorization.tests.test_user import json_testdata, TestUser
from amazon.a_models import SpapiCredential

from dashboard.tests.test_store import TestStoreProfile
from sp_api.api import Orders
from sp_api.base.marketplaces import Marketplaces


# Create your tests here.
class TestSpapiCredential(TestStoreProfile):
    def setUp(self):
        super(TestSpapiCredential,self).setUp()
        self.credential = SpapiCredential.objects.create(
            **{
                "user" : self.test_user, "store" : self.store,
               **json_testdata["amazon"]
            }
        )
        self.assertIsNotNone(self.credential)
        
    def test_report_client(self):
        spapi_credential = self.credential.get_credentials(
            user=self.test_user,store_slug=self.store.slug
        )
        order_client = Orders(
            credentials= dict(
                refresh_token = spapi_credential.refresh_token,
                lwa_app_id = spapi_credential.client_id,
                lwa_client_secret = spapi_credential.client_secret,
            ),
            marketplace=Marketplaces.IN
        )
        order = order_client.get_order("405-1181345-7106760")