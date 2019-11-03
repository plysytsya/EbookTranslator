import os
import sys
import unittest
import warnings

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(THIS_DIR)
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
sys.path.append(SCRIPTS_DIR)

from translator import Translator, GoogleEngine


def get_mock_text():
    path = os.path.join(THIS_DIR, "test_data", "zen_en.txt")
    with open(path) as file:
        return file.read()


class TranslatorTest(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.translator = Translator(source_language="en", target_language="de", engine="Google")

    def test_1_set_engine(self):
        self.translator.set_engine("Google")
        self.assertTrue(self.translator.engine)

    def test_2_translate(self):
        text = get_mock_text()
        translation = self.translator.translate(text)
        self.assertTrue(isinstance(translation, str))

    def test_3_quit(self):
        self.translator.quit()


class GoogleEngineTest(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.engine = GoogleEngine(source_language="en", target_language="de")

    def test_1_get_supported_locales(self):
        locales = self.engine.get_supported_locales()
        self.assertTrue(isinstance(locales, list))
        self.assertIn("en", locales, "English language must be supported.")

    def test_2_translate(self):
        text = get_mock_text()
        translation = self.engine.translate(text)
        self.assertIsInstance(translation, str)


if __name__ == '__main__':
    unittest.main(verbosity=3)
