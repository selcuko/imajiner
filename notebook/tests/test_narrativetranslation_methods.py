from ..models import Narrative, NarrativeTranslation
from .common import TestCase


class NarrativeTranslationMethodTests(TestCase):

    def test_title_null(self):
        self.narrative.title = None
        self.narrative.save()
        self.assertIs(self.narrative.title, None)

        self.narrative.title = ''
        self.narrative.save()
        self.assertIs(self.narrative.title, None)
    
    def test_title_valid(self):
        self.narrative.title = "I am a title"
        self.narrative.save()
        self.assertIsInstance(self.narrative.title, str)
    
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
    
    def test_languages(self):
        # TODO: this case must be moved to test_narrative_methods
        master = Narrative.objects.create(author=self.user)
        narrative_tr = NarrativeTranslation.objects.create(master=master, language='tr')
        narrative_fr = NarrativeTranslation.objects.create(master=master, language='fr')
        self.assertEqual(set(master.languages), set(['fr', 'tr']))

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
    


    