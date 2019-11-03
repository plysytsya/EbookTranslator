import os
import sys
import unittest
import warnings

from hypothesis import given
from hypothesis.strategies import text

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(THIS_DIR)
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
sys.path.append(SCRIPTS_DIR)

from sentence_mapper import SentenceMapper


def get_mock_text(path):
    with open(path) as file:
        return file.read()


class SentenceMapperTest(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        path_en = os.path.join(THIS_DIR, "test_data", "zen_en.txt")
        path_de = os.path.join(THIS_DIR, "test_data", "zen_de.txt")
        self.mapper = SentenceMapper(path_en, path_de, "en", "de")

    @given(text(), text())
    def test_1_get_jaccard_similarity(self, text_a, text_b):
        similarity = self.mapper.get_jaccard_similarity(text_a, text_b)
        self.assertIsInstance(similarity, float)

    def test_2_prepare_tokens(self):
        tokens_a, tokens_b = self.mapper.prepare_tokens()
        self.assertIsInstance(tokens_a, list)
        self.assertIsInstance(tokens_b, list)
        self.assertTrue(len(tokens_a) > 0)
        self.assertTrue(len(tokens_a) > 0)

    def test_3_make_translations(self):
        test_tokens = ["hello, world!", "good morning"]
        translations = self.mapper.make_translations(test_tokens)
        self.assertEqual(len(translations), len(test_tokens))
        self.assertIn("Welt", translations[0])
        self.assertIn("Morgen", translations[1])

    def test_4_


if __name__ == '__main__':
    unittest.main(verbosity=3)
