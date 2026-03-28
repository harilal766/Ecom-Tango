from django.test import TestCase

from authorization.tests.test_user import json_testdata, TestUser
from dashboard.tests.test_models import TestBaseCredential
from shopify.sh_models import ShopifyApiCredential


# Create your tests here.
class TestShopifyCreds(TestBaseCredential):
    def setUp(self):
        super(TestShopifyCreds,self).setUp()
        self.shopify_test_instance = ShopifyApiCredential.objects.create(
            **{
                "user" : self.test_user, "store" : self.test_store,
                **json_testdata["api_credentials"]["shopify"][0]
            }
        )
        self.shopify_test_credentials = self.shopify_test_instance.get_the_credentials()
        self.assertIsNotNone(self.shopify_test_instance)
        
    def test_shopify_credentials(self):
        self.assertIsNotNone(self.shopify_test_credentials)