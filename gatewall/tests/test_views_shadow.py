from django.test import TestCase, RequestFactory
from django.shortcuts import reverse
from uuid import uuid1
from identity.models import Shadow
from ..views import Auth
from json import loads
import logging

logger = logging.getLogger('django.request')
logger.setLevel(logging.FATAL)


class ShadowViewsTests(TestCase):
    fp0 = uuid1()
    fp1 = uuid1()
    gatewall = reverse('gatewall:auth')

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.request = cls.factory.get(reverse('gatewall:auth'))


    def setUp(self):
        pass
    
    def post(self, body={}):
        return self.client.post(self.gatewall, body)

    def jsonify(self, response):
        return loads(str(response.content, encoding='utf-8'))


    def test_nothing_supplied(self):
        response = self.post()
        self.assertEqual(response.status_code, 400)

        response = self.post()
        self.assertEqual(response.status_code, 400)
    

    def test_invalid_body(self):
        response = self.post({ 'action': 'username-availability' })
        self.assertEqual(response.status_code, 400)

        response = self.post({ 'action': 'username-availability', 'username': '' })
        self.assertEqual(response.status_code, 400)
        
        response = self.post({ 'action': 'username-availability', 'username': 55 })
        self.assertEqual(response.status_code, 400)


    def test_invalid_action(self):
        response = self.post({ 'action': 'dummy' })
        self.assertEqual(response.status_code, 400)

        response = self.post({ 'action': 'dummy', 'dummy': 'dummy' })
        self.assertEqual(response.status_code, 400)


    def test_fingerprint_operations(self):
        fp1, fp2 = str(uuid1()), str(uuid1())

        # not recognized
        response = self.post({
            'action': 'shadow-check',
            'fingerprint': fp1
        })
        json = self.jsonify(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn('found', json.keys())
        self.assertFalse(json.get('found'))

        # recognized
        Shadow.create_shadow(self.request, fp1)
        response = self.post({
            'action': 'shadow-check',
            'fingerprint': fp1
        })
        json = self.jsonify(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn('found', json.keys())
        self.assertTrue(json.get('found'))


    def test_register_login(self):
        response = self.post({
            'fingerprint': self.fp0,
            'action': 'shadow-register',
        })
        json = self.jsonify(response)
        self.assertEqual(response.status_code, 200, json)
        return
        response = self.post({
            'fingerprint': self.fp0,
            'action': 'shadow-register',
        })
        json = self.jsonify(response)
        self.assertEqual(response.status_code, 400, json)

        response = self.post({
            'fingerprint': '',
            'action': 'shadow-register',
        })
        self.assertEqual(response.status_code, 400, json)


