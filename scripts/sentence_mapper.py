from text_tokenizer import TextTokenizer
from translator import Translator


class SentenceMapper:

    """The SentenceMatchEngine takes two sources: text a and text b.
    Both sources must represent the same text in different languages.
    The goal is to match sentences of the two languages.
    To achieve this it first translates text a validating the translated
    sentences against sentences of text b. The core metric is a similarity-index.
    If a given similarity-threshold is not reached it falls back to the translated sentence.
    """
    def __init__(self, text_a, text_b, source_language, target_language):
        self.text_a = text_a
        self.text_b = text_b
        self.translator = Translator(source_language, target_language)

    def prepare_tokens(self):
        tokens_a = TextTokenizer(self.text_a).tokenize()
        tokens_b = TextTokenizer(self.text_b).tokenize()
        return tokens_a, tokens_b

    def make_translations(self, tokens_a):
        return [
            self.translator.translate(token)
            for token in tokens_a
        ]

    def compare(self, translations, tokens_b):
        pass

    def get_jaccard_similarity(self, str1, str2):
        if str1 == "" or str2 == "":
            return 0.0
        else:
            a = set(str1.split())
            b = set(str2.split())
            c = a.intersection(b)
            return float(len(c)) / (len(a) + len(b) - len(c))

    def main(self):
        tokens_a, tokens_b = self.prepare_tokens()
        translations = self.make_translations()
