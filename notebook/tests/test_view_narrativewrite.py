from .common import TestCase
from django.shortcuts import reverse
from notebook.models import NarrativeTranslation
from uuid import uuid1

class NarrativeDetail(TestCase):

    def setUp(self):
        super().setUp()
        self.logout()


    def test_new_anonymous_get(self):
        response = self.client.get(reverse('notebook:write'))
        self.assertEqual(response.status_code, 302)
    
    
    def test_new_anonymous_post(self):
        response = self.client.get(reverse('notebook:write'))
        self.assertEqual(response.status_code, 302)


    def test_new_get(self):
        self.login()
        response = self.client.get(reverse('notebook:write'))
        self.assertEqual(response.status_code, 200)
    

    def test_new_post_invalid(self):
        self.login()
        response = self.client.post(reverse('notebook:write'),{})
        self.assertEqual(response.status_code, 400)
        

    def test_sketch_anonymous_get(self):
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        self.assertEqual(response.status_code, 302)
    

    def test_sketch_anonymous_get_404(self):
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': str(uuid1())}))
        self.assertEqual(response.status_code, 302)
    

    def test_sketch_anonymous_post(self):
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        self.assertEqual(response.status_code, 302)
    

    def test_sketch_anonymous_post_404(self):
        response = self.client.post(reverse('notebook:sketch', kwargs={'uuid': str(uuid1())}))
        self.assertEqual(response.status_code, 302)
    

    def test_sketch_get(self):
        self.login()
        response = self.client.get(reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}))
        self.assertEqual(response.status_code, 200)


    def test_sketch_get_404(self):
        self.login()
        response = self.client.get(reverse('narrative:sketch', kwargs={'uuid': str(uuid1())}))
    

    def test_sketch_post_autosave(self):
        self.login()
        response = self.client.post(
            reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}),
            {
                'uuid': self.narrative.uuid,
                'title': '',
                'body': '',
                'action': 'autosave',
            })
        self.assertEqual(response.status_code, 200)


    def test_sketch_post_submit(self):
        self.login()
        narrative = NarrativeTranslation()
        narrative.save(author=self.user)
        response = self.client.post(
            reverse('notebook:sketch', kwargs={'uuid': narrative.uuid}),
            {
                'uuid': narrative.uuid,
                'title': '...',
                'body': '...',
                'action': 'submit',
            })
        narrative.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(narrative.sketch)

    
    def test_sketch_post_invalid(self):
        self.login()

        response = self.client.post(
            reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}),
            {
                'uuid': self.narrative.uuid,
                'title': '',
                'body': '',
                'action': 'i-am-not-vaid',
            })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}),
            {
                'uuid': self.narrative.uuid,
                'action': 'i-am-invalid',
            })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            reverse('notebook:sketch', kwargs={'uuid': self.narrative.uuid}),
            {})
        self.assertEqual(response.status_code, 400)


    def test_add_translation(self):
        self.login()
        response = self.client.get(
            reverse('narrative:translate', kwargs={'uuid': self.narrative.uuid}),
            follow=True)
        self.assertEqual(response.status_code, 200)