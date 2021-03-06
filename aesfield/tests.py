import os
import tempfile

from django.conf import settings

minimal = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase'
        }
    },
    'AES_KEYS': {'foo': os.path.join(os.path.dirname(__file__), 'sample.key')}
}

if not settings.configured:
    settings.configure(**minimal)

from django.db import models
from django.test import TestCase

from .field import AESField, EncryptedField
from .management.commands.generate_aes_keys import Command, CommandError


class TestModel(models.Model):
    key = AESField(max_length=255)


class TestBasic(TestCase):

    def test_lookup(self):
        with self.assertRaises(EncryptedField):
            TestModel.objects.filter(key='asd')

    def test_no_prefix(self):
        with self.assertRaises(ValueError):
            AESField(aes_prefix='')

    def test_get_key(self):
        key = 'some-super-secret-key'
        fn = tempfile.NamedTemporaryFile()
        fn.write(key)
        fn.flush()
        with self.settings(AES_KEYS={'default': fn.name}):
            assert AESField().get_aes_key() == 'some-super-secret-key'

    def test_generate_fails(self):
        with self.assertRaises(CommandError):
            Command().handle()

    # TODO: figure out how to do the rest of the tests here.
    # Remaining tests are in solitude
