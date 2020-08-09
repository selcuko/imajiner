from django.test import TestCase
from django.shortcuts import reverse
from .models import *
from model_bakery import baker

class NarrativeViews(TestCase):

    def setUp(self):
        self.nqs = Narrative.objects.all()
        if len(self.nqs) < 20:
            objects = baker.make(
                'notebook.Narrative',
                _fill_optional=['author', 'body'],
                make_m2m=True,
                _quantity=20,
            )
        self.nqs = Narrative.objects.all()

    def test_narrative_detail(self):
        for n in self.nqs[::5]:
            r = self.client.get(
                reverse('narrative:detail', kwargs={'slug':n.slug})
            )
            self.assertEqual(r.status_code, 200, 'narrative:detail GET returned non-200')
    
    def test_narrative_list(self):
        for i in range(1, 10):
            r = self.client.get(
                f'{reverse("narrative:list")}?page={i}'
            )
            if 'infinite-more-link' not in r.content.decode():
                break
            self.assertEqual(r.status_code, 200, 'narrative:list GET returned non-200')
