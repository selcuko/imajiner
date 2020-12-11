from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

class FlatpagesTest(TestCase):
    @classmethod
    def setUpTestData(cls): pass   #  overriding these methods as this testcase does not 
    def setUp(self): pass          #  require db data

    def test_about(self):
        response = self.client.get(reverse('explore:about'))
        self.assertEqual(response.status_code, 200)

    