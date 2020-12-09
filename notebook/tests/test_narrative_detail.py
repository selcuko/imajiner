from imajiner.tests import TestCase
from django.shortcuts import reverse

class NarrativeDetail(TestCase):

    def test_narrative_detail_anonymous(self):
        self.logout()
        response = self.client.get(reverse('narrative:detail', kwargs={'slug': self.narratives[0].slug}))
        assert response.status_code == 200, 'Status Code not 200 when accessing NarrativeDetail'
        
