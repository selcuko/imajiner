from django.test import TestCase
from django.shortcuts import reverse
from model_bakery import baker
from ..models import NarrativeTranslation, Narrative
from ..exceptions import AbsentMasterException

class NarrativeTranslationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make('auth.User')
        cls.user.set_password(cls.user.password)


    def test_save_unvalid(self):
        narrative = NarrativeTranslation()
        with self.assertRaises(AbsentMasterException):
            narrative.save()
    
    def test_autosave_unvalid(self):
        narrative = NarrativeTranslation()
        with self.assertRaises(AbsentMasterException):
            narrative.autosave()
    
    def test_save_with_author(self):
        narrative = NarrativeTranslation()
        try:
            narrative.save(author=self.user)
        except Exception as exc:
            self.fail(f'NarrativeTranslation save method failed with {exc!r}')
    
    def test_save_redundant_author(self):
        master = Narrative(author=self.user)
        master.save()
        narrative = NarrativeTranslation(master=master)
        try:
            narrative.save(author=self.user)
        except Exception as exc:
            self.fail(f'NarrativeTranslation save method failed with {exc!r}')
    
    def test_save_valid(self):
        master = Narrative(author=self.user)
        master.save()
        narrative = NarrativeTranslation(master=master)
        try:
            narrative.save()
        except Exception as exc:
            self.fail(f'NarrativeTranslation save method failed with {exc!r}')
    
    def test_save_version(self):
        narrative = NarrativeTranslation()
        try:
            narrative.save(author=self.user)
        except Exception as exc:
            self.fail(f'NarrativeTranslation save method failed with {exc!r}')
        else:
            self.assertIsNotNone(narrative.latest)
    

    def test_autosave_valid(self):
        narrative = NarrativeTranslation()
        try:
            narrative.autosave(author=self.user)
        except Exception as exc:
            self.fail(f'NarrativeTranslation save method failed with {exc!r}')
    

    def test_autosave_version_number(self):
        narrative = NarrativeTranslation()
        try:
            narrative.autosave(author=self.user)
            narrative.publish()
        except Exception as exc:
            self.fail(f'NarrativeTranslation save method failed with {exc!r}')
        else:
            self.assertEqual(narrative.latest.version, 1)
    

    def test_publish_unvalid(self):
        narrative = NarrativeTranslation()
        with self.assertRaises(AbsentMasterException):
            narrative.publish()
    

    def test_publish_valid(self):
        narrative = NarrativeTranslation()
        try:
            narrative.publish(author=self.user)
        except Exception as exc:
            self.fail(f'NarrativeTranslation save method failed with {exc!r}')
        else:
            self.assertFalse(narrative.sketch)
            self.assertFalse(narrative.latest.sketch)
    

    def test_get_absolute_url(self):
        narrative = NarrativeTranslation()
        narrative.save(author=self.user)
        self.assertEqual(narrative.get_absolute_url(), reverse('narrative:sketch', kwargs={'uuid':narrative.uuid}))
        narrative.sketch=False
        narrative.save()
        self.assertEqual(narrative.get_absolute_url(), reverse('narrative:detail', kwargs={'slug': narrative.slug}))


