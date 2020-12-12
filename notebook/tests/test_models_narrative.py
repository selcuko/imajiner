from django.test import TestCase
from django.shortcuts import reverse
from model_bakery import baker
from datetime import datetime
from ..models import Narrative, NarrativeTranslation
from ..exceptions import AbsentMasterException


class NarrativeModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make('auth.User')
        cls.user.set_password(cls.user.password)
        cls.master = Narrative.objects.create(author=cls.user)


    def setUp(self):
        narrative_tr = NarrativeTranslation.objects.create(master=self.master, language='tr')
        narrative_fr = NarrativeTranslation.objects.create(master=self.master, language='fr')


    def test_languages(self):
        # TODO: this case must be moved to test_narrative_methods
        self.assertEqual(set(self.master.languages), set(['fr', 'tr']))


    def test_title(self):
        self.assertIsNone(self.master.title)
        self.master.translations.update(title='Title')
        self.assertIn(self.master.title, [t.title for t in self.master.translations.all()])
    

    def test_published_at(self):
        self.master.translations.all().delete()
        self.assertIsNone(self.master.published_at)
        narrative_tr = NarrativeTranslation.objects.create(sketch=False, master=self.master)
        self.assertIsInstance(self.master.published_at, datetime)
    

    def test_is_published(self):
        self.assertFalse(self.master.is_published)
        n = self.master.translations.first()
        n.sketch = False
        n.save()
        self.assertTrue(self.master.is_published)
        

    def test_edited_at(self):
        self.assertIsNotNone(self.master.edited_at)
        self.master.translations.all().delete()
        self.assertIsNone(self.master.edited_at)


