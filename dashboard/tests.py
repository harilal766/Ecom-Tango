from django.test import TestCase
from .d_models import BaseCredential

# Create your tests here.
class TestBaseCredential(TestCase):
    def setUp(self):
        BaseCredential.objects.create()