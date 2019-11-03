import time
import datetime

import googletrans

from browser import Browser
from text_tokenizer import TextTokenizer


class Translator:
    def __init__(self, source_language, target_language, engine):
        self.source_language = source_language
        self.target_language = target_language
        self.set_engine(engine)

    def set_engine(self, name):
        engines = ["Google", "DeepL"]
        assert name in engines, f"{name} is not a supported engine."
        if name == "Google":
            self.engine = GoogleEngine(self.source_language, self.target_language)
        elif name == "DeepL":
            self.engine = DeepLEngine(self.source_language, self.target_language)

    def translate(self, text):
        return self.engine.translate(text)

    def quit(self):
        try:
            self.engine.browser.quit()
        except AttributeError:
            pass


class GoogleEngine:
    """Free google-translate client provided by:
    https://github.com/ssut/py-googletrans """

    def __init__(self, source_language, target_language):
        print("Initializing Google translator")
        self.source_language = source_language
        self.target_language = target_language
        self.engine = googletrans.Translator()

    def get_supported_locales(self):
        locales = [locale for language, locale, in googletrans.LANGCODES.items()]
        return locales

    def translate(self, text):
        translation = self.engine.translate(
            text, src=self.source_language, dest=self.target_language
        )
        return translation.text


class DeepLEngine:
    def __init__(self, source_language, target_language):
        print("Initializing DeepL translator")
        self.browser = Browser(headless=True)
        self.source_language = source_language.upper()
        self.target_language = target_language.upper()
        self.prepare()

    def get_supported_locales(self):
        locales = ["EN", "DE", "FR", "ES", "PT", "IT", "NL", "PL", "RU"]
        return [locale.lower() for locale in locales]

    def prepare(self):
        self.browser.driver.get("https://www.deepl.com/translator")
        self.select_source_language()
        self.select_target_language()

    def select_source_language(self):
        self.open_language_selection(0)
        source_language_menu = self.get_language_menu("source")
        self.click_target_language(source_language_menu, self.source_language)

    def select_target_language(self):
        self.open_language_selection(1)
        target_language_menu = self.get_language_menu("target")
        self.click_target_language(target_language_menu, self.target_language)

    def open_language_selection(self, direction):
        self.browser.driver.find_elements_by_class_name("lmt__language_select__active")[
            direction
        ].click()

    def get_language_menu(self, direction):
        target_lang_menu = self.browser.driver.find_element_by_xpath(
            f'//*[@dl-test="translator-{direction}-lang-list"]'
        )
        return target_lang_menu

    def click_target_language(self, language_menu, language_code):
        buttons = language_menu.find_elements_by_tag_name("button")
        for button in buttons:
            if button.get_attribute("dl-value") == language_code:
                print(f"Choosing language code {language_code}")
                button.click()
                time.sleep(1)

    def translate(self, text):
        self.fill_input_field(text)
        translation = self.get_translation(text)
        self.clear_input()
        return translation

    def fill_input_field(self, text):
        input_field = self.get_input_field()
        input_field.send_keys(text)

    def get_input_field(self):
        return self.browser.driver.find_element_by_xpath(
            '//*[@dl-test="translator-source-input"]'
        )

    def get_translation(self, text):
        self.wait_for_translation(text)
        return self.read_output()

    def wait_for_translation(self, original, timeout=60, seconds=3):
        start = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=timeout)
        self.wait_until_equal_number_of_words(original, self.read_output())
        while True:
            old_output = self.read_output()
            time.sleep(seconds)
            new_output = self.read_output()
            if '[...]' in new_output:
                time.sleep(15)
            if new_output == old_output and new_output != "":
                return True
            if datetime.datetime.now() >= start + timeout:
                break

    def wait_until_equal_number_of_words(self, text_1, text_2, timeout=15):
        start = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=timeout)
        while True:
            if self.is_equal_number_of_words(text_1, text_2, tolerance=1) is True:
                break
            if datetime.datetime.now() >= start + timeout:
                break

    def is_equal_number_of_words(self, text_1, text_2, tolerance=1):
        words_1 = TextTokenizer(text_1).tokenize(tokens="words")
        words_2 = TextTokenizer(text_2).tokenize(tokens="words")
        if len(words_1) >= len(words_2) - tolerance:
            return True
        else:
            return False

    def clear_input(self):
        input_field = self.get_input_field()
        input_field.click()
        input_field.clear()
        self.wait_until_clear_output()

    def wait_until_clear_output(self, timeout=30):
        start = datetime.datetime.now()
        timeout = datetime.timedelta(seconds=timeout)
        while True:
            output = self.read_output()
            if output == '':
                break
            if datetime.datetime.now() >= start + timeout:
                break

    def read_output(self):
        textarea = self.get_output_textarea()
        return textarea.get_attribute("value")

    def get_output_textarea(self):
        output_box = self.browser.driver.find_elements_by_class_name(
            "lmt__inner_textarea_container"
        )[1]
        return output_box.find_element_by_tag_name("textarea")
