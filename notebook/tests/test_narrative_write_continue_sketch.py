from imajiner.tests import TestCase
from django.shortcuts import reverse
from notebook.models import NarrativeTranslation

class NarrativeContinueSketch(TestCase):

    def setUp(self): 
        self.narrative = self.narratives.first()

    def test_get_narrative_write_anonymous(self):
        self.logout()
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        assert response.status_code in [302, 403]
    
    def test_get_narrative_write_authorized(self):
        self.login()
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        assert response.status_code == 200
    
    def test_post_narrative_write_authorized(self):
        self.login()
        response = self.client.post(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        assert response.status_code == 400
