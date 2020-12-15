from django.test import TestCase
from django.shortcuts import reverse
from model_bakery import baker
from ..models import Narrative, NarrativeTranslation, NarrativeVersion
from ..exceptions import ReadonlyException
import logging

logger = logging.getLogger('notebook.models')
logger.setLevel(logging.FATAL)

class NarrativeTranslationModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = baker.make('auth.User')
        cls.user.set_password(cls.user.password)
        cls.narrative = NarrativeTranslation()
        cls.narrative.save(author=cls.user)
        cls.last_version = 4
    

    def setUp(self):
        for i in range(self.last_version):
            self.narrative.title = f'Iteration-{i+1}'
            self.narrative.autosave()
            self.narrative.publish()
        self.narrative.autosave()
        self.version = self.narrative.latest
        print(self.version.sketch, self.version.readonly)


    def test_title(self):
        self.assertIsInstance(str(self.version), str)
    
    
    def test_version_number(self):
        self.assertEqual(self.version.version, self.last_version)
    

    def test_reference_with_save(self):
        try:
            self.version.reference(self.narrative, save=True, overwrite=True)
        except Exception as exc:
            self.fail(f'NarrativeVersion failed with {exc!r}')
    

    def test_method_archive(self):
        try:
            self.version.archive()
        except Exception as exc:
            self.fail(f'NarrativeVersion failed with {exc!r}')
        else:
            with self.assertRaises(ReadonlyException):
                self.version.save()