from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelsTestCase(TestCase):
    def test_dashboard_creation(self):
        self.assertEqual(len(models.Dashboard.objects.all()), 0)
        get_user_model().objects.create(username='testing')
        self.assertEquals(len(models.Dashboard.objects.all()), 1)
