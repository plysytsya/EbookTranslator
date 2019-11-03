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

from ebook_translator import EbookTranslator


def get_mock_text(path):
    with open(path) as file:
        return file.read()


class SentenceMapperTest(unittest.TestCase):

    def setUp(self):
        path = os.path.join(THIS_DIR, "test_data", "zen_en.txt")
        self.ebook_translator = EbookTranslator(path, "en", "de")

    def test_1_translate(self):
        self.ebook_translator.translate()

    def test_2_write_to_file(self):
        out_dir = os.path.join(THIS_DIR, "test_data")
        file_name = "translation.txt"
        mock_text = "Lorem ipsum dolorem"
        self.ebook_translator.write_to_file(mock_text, os.path.join(out_dir, file_name))
        self.assertIn(file_name, os.listdir(out_dir))

    def tearDown(self):
        self.ebook_translator.quit()


if __name__ == '__main__':
    unittest.main(verbosity=3)
