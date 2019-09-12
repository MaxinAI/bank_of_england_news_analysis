from unittest import TestCase
from model.helpers import found


class TestFound(TestCase):
    def test_found(self):
        texts = ['abc', 'a', 'vc', 'bbd']
        keys = ['a', 'b', 'c', 'd']

        self.assertEqual(True, found(texts, keys, 'all', True))
        self.assertEqual(True, found(texts, keys, 'any', True))
        self.assertEqual(False, found(texts, keys, 'none', True))

        self.assertEqual(False, found(texts, keys, 'all', False))
        self.assertEqual(True, found(texts, keys, 'any', False))
        self.assertEqual(False, found(texts, keys, 'none', False))
