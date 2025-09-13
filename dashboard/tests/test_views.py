from django.test import TestCase
from dashboard.d_views import Dashboard
from django.urls import reverse

class TestDashboard(TestCase):
    def setUp(self):
        self.dash_client = Dashboard()
        
class Store(TestCase):
    def test_get(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)