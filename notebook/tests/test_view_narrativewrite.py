from .common import TestCase
from django.shortcuts import reverse
from notebook.models import NarrativeTranslation

class NarrativeDetail(TestCase):

    def test_get_narrative_write_anonymous(self):
        self.logout()
        response = self.client.get(reverse('narrative:write'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('gatewall:auth'), response.url)
    
    def test_get_narrative_write_authorized(self):
        self.login()
        response = self.client.get(reverse('narrative:write'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_narrative_write_authorized_bad_request(self):
        self.login()
        response = self.client.post(reverse('narrative:write'))
        self.assertEqual(response.status_code, 400)

    def test_continue_sketch_get(self):
        self.logout()
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        self.assertEqual(response.status_code, 302)
    
    def test_continue_sketch_post(self):
        self.login()
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        self.assertEqual(response.status_code, 200)
    

    

