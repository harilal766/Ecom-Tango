from django.test import TestCase

from authorization.tests.test_user import json_testdata, TestUser
from shopify.sh_models import ShopifyApiCredential


# Create your tests here.
class TestShopifyCreds():
    def setUp(self):
        super(TestShopifyCreds,self).setUp()
        self.shopify_test_instance = ShopifyApiCredential.objects.create(
            **{
                "user" : self.test_user, "store" : self.test_store,
                **json_testdata["shopify"]
            }
        )
        self.assertIsNotNone(self.shopify_test_instance)
        self.assertIsNotNone(self.shopify_test_instance.get_the_credentials())
        
    def test_shopify_credentials(self):
        self.assertIsNotNone(self.shopify_test_instance.get_the_credentials())
        
    



