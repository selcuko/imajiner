from django.test import TestCase, RequestFactory
from django.shortcuts import reverse
from uuid import uuid1
from identity.models import Shadow
from ..views import Auth

class ShadowViewsTests(TestCase):
    fingerprint0 = uuid1()
    fingerprint1 = uuid1()

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.request = cls.factory.get(reverse('gatewall:auth'))
        cls.shadow = Shadow.create_shadow(cls.request, cls.fingerprint0)

    def setUp(self):
        pass
    

    def test_check_404(self):
        response = self.client.post(reverse('gatewall:auth'), {
            'action': 'shadow-check',
            'fingerprint': self.fingerprint0,
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf-8'),
            {'found': False}
        )
    

    def test_check_found(self):
        response = self.client.post(reverse('gatewall:auth'), {
            'action': 'shadow-check',
            'fingerprint': self.fingerprint0,
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf-8'), 
            {'found': True}
        )


    def test_check_invalid(self):
        response = self.client.post(reverse('gatewall:auth'), {
            'action': 'shadow-check',
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('gatewall:auth'), {})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('gatewall:auth'), {
            'action': 'dummy-action',
        })
        self.assertEqual(response.status_code, 400)