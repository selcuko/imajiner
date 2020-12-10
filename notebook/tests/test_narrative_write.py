from imajiner.tests import TestCase
from django.shortcuts import reverse
from notebook.models import NarrativeTranslation

class NarrativeDetail(TestCase):

    def test_narrative_write_anonymous(self):
        self.logout()
        response = self.client.get(reverse('narrative:write'))
        assert response.status_code == 302
    
    def test_narrative_write_authorized(self):
        self.login()
        response = self.client.get(reverse('narrative:write'))
        assert response.status_code == 200