from django.test import TestCase
from dashboard.d_views import Dashboard


class TestDashboard(TestCase):
    def setUp(self):
        self.dash_client = Dashboard()
        