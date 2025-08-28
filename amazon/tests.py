from django.test import TestCase
from .a_views import Spapi_Report
from .a_models import SpapiCredential

# Create your tests here.

class TestSpapi_Report(TestCase):
    report_instance = Spapi_Report()
    def test_get_spapi_credentials(self):
        amazon_store = SpapiCredential.objects.all()

        self.assertEqual(amazon_store.count(), 0)
        