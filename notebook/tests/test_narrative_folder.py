from imajiner.tests import TestCase
from django.shortcuts import reverse
from notebook.models import NarrativeTranslation

class NarrativeFolder(TestCase):

    def test_folder_unauthorized(self):
        self.logout()
        response = self.client.get(reverse('narrative:folder'))
        assert response.status_code == 302
    
    def test_folder_authorized(self):
        self.login()
        response = self.client.get(reverse('narrative:folder'))
        expected = NarrativeTranslation.objects.filter(sketch=True, master__author=self.user)
        assert response.status_code == 200, 'Status Code not OK when accessed FolderView'
        
    
    def test_folder_content(self):
        self.login()
        response = self.client.get(reverse('narrative:folder'))
        assert response.context.get('sketches', None) is not None
        assert set(response.context.get('sketches', None)) == set(expected)
        