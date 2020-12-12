from .common import TestCase
from django.shortcuts import reverse
from notebook.models import NarrativeTranslation

class NarrativeFolder(TestCase):

    def test_folder_unauthorized(self):
        self.logout()
        response = self.client.get(reverse('narrative:folder'))
        assert response.status_code == 302, f'Status Code {response.status_code} when accessed FolderView anonymously.'
    
    def test_folder_authorized(self):
        self.login()
        response = self.client.get(reverse('narrative:folder'))
        assert response.status_code == 200, f'Status Code {response.status_code} when accessed FolderView authorized.'
        
    
    def test_folder_content(self):
        self.login()
        expected = NarrativeTranslation.objects.filter(sketch=True, master__author=self.user)
        response = self.client.get(reverse('narrative:folder'))
        assert response.context.get('sketches', None) is not None, f'Context of FolderView does not contain sketches.'
        assert set(response.context.get('sketches', None)) == set(expected), f'FolderView does not contain all sketches of the author.'
        