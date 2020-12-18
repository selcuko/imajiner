from django.test import TestCase
from django.shortcuts import reverse
from model_bakery import baker
from ..models import Narrative, NarrativeTranslation
from ..exceptions import AbsentMasterException

class NarrativeTranslationModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make('auth.User')
        cls.user.set_password(cls.user.password)
        cls.narrative = NarrativeTranslation()
        cls.narrative.save(author=cls.user)


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
    
    def test_publish_without_autosave(self):
        narrative = NarrativeTranslation()
        try:
            narrative.publish(author=self.user)
        except Exception as exc:
            self.fail(f'NarrativeTranslation publish method failed with {exc!r}')
    
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
        self.assertIsNone(narrative.get_absolute_url())
        narrative.sketch=False
        narrative.save()
        self.assertEqual(narrative.get_absolute_url(), reverse('narrative:detail', kwargs={'slug': narrative.slug}))


    def test_title_null(self):
        self.narrative.title = None
        self.narrative.save()
        self.assertIs(self.narrative.title, None)
        self.assertIsInstance(str(self.narrative), str)

        self.narrative.title = ''
        self.narrative.save()
        self.assertIs(self.narrative.title, None)
        self.assertIsInstance(str(self.narrative), str)
    

    def test_title_valid(self):
        self.narrative.title = "I am a title"
        self.narrative.save()
        self.assertIsInstance(self.narrative.title, str)
        self.assertIsInstance(str(self.narrative), str)
    

    def test_body_null(self):
        self.narrative.body = None
        self.narrative.save()
        self.assertIs(self.narrative.body, None)

        self.narrative.body = ''
        self.narrative.save()
        self.assertIs(self.narrative.body, None)
    

    def test_body_valid(self):
        self.narrative.body = "I am THE body"
        self.narrative.save()
        self.assertIsInstance(self.narrative.body, str)
    

    def test_is_published(self):
        narrative = NarrativeTranslation()
        narrative.save(author=self.user)
        self.assertFalse(narrative.is_published)

        narrative.publish()
        self.assertTrue(narrative.is_published)
    

    def test_language_detection(self):
        narrative = NarrativeTranslation()
        narrative.sketch = False
        narrative.body = """The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. """
        narrative.save(author=self.user)
        self.assertEqual(narrative.language, 'en')
    

    def test_language_unclassified(self):
        narrative = NarrativeTranslation()
        narrative.sketch = False
        narrative.body = """2c4ol4ekDpQeb01mA1yIKIDn0paTG4DnfAFDPsmq31Hf2wWkdZBXgrrygO8o"""
        narrative.save(author=self.user)
        self.assertIs(narrative.language, None)
    
    
    def test_autosave_with_latest_and_vcs(self):
        # TODO: distribute this case
        narrative = NarrativeTranslation()
        try:
            narrative.autosave(author=self.user)
            narrative.autosave()
            self.assertFalse(narrative.latest.readonly)
            narrative.autosave(author=self.user)
            narrative.autosave()
            narrative.publish()
            self.assertTrue(narrative.latest.readonly)
            narrative.autosave(author=self.user)
            narrative.publish()

        except Exception as exc:
            self.fail(f'NarrativeTranslation methods failed with {exc!r}')
        
        else:
            self.assertEqual(narrative.latest.version, 2)
            self.assertEqual(narrative.version, 2)
    

