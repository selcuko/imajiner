from ..models import NarrativeTranslation
from .common import TestCase


class NarrativeTranslationMethodTests(TestCase):

    def test_title_null(self):
        self.narrative.title = None
        self.narrative.save()
        self.assertIs(self.narrative.title, None)
    
    def test_title_valid(self):
        self.narrative.title = "I am a title"
        self.narrative.save()
        self.assertIsInstance(self.narrative.title, str)
 