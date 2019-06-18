from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from utils.views import health


class UtilTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_health_view(self):
        request = self.factory.get(reverse("utils:health"))
        response = health(request)
        self.assertEqual(response.status_code, 200)
