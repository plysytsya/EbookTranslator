import os
import sys
import unittest

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(THIS_DIR)
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
sys.path.append(SCRIPTS_DIR)

from ebook import Ebook


class EbookTest(unittest.TestCase):

    def setUp(self):
        path_to_text = os.path.join(THIS_DIR, "test_data", "zen_en.txt")
        self.ebook = Ebook(path_to_text)

    def test_1_read(self):
        self.ebook.read()
        self.assertIsInstance(self.ebook.content, str)

    def test_2_split_book_into_sentences(self):
        self.ebook.split_into_sentences()
        self.assertIsInstance(self.ebook.sentences, list)


if __name__ == '__main__':
    unittest.main(verbosity=3)
