from django.test import TestCase
from django.contrib.auth.models import User
from .models import *

class TagManager(TestCase):

    def setUp(self):
        if not User.objects.filter(username='tester').exists():
            self.user = User.objects.create(username='tester', password='')
        else:
            self.user = User.objects.get('tester')

    
    def test_check_related_models(self):
        self.assertIsInstance(self.user.tags, UserTagManager)


    def test_abstract_tag_not_exists(self):
        try:
            self.user.tags.delta('non-existent-tag', 4)
        except AbstractTag.DoesNotExist:
            a = AbstractTag.objects.create(name='existent-tag')
            self.user.tags.delta('existent-tag', 1)

    
    def test_sth(self):
        pass

