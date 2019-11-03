import os

from tqdm import tqdm

from ebook import Ebook
from translator import Translator


class EbookTranslator:
    def __init__(self, path, source_language, target_language, engine="Google"):
        self.source_language = source_language
        self.target_language = target_language
        self.ebook = Ebook(path)
        self.set_out_path()
        self.set_counter_path()
        self.set_start_point()
        self.translator = Translator(source_language, target_language, engine)

    def translate(self):
        for counter, original_sentence in enumerate(tqdm(self.ebook.sentences)):
            translated_sentence = self.translator.translate(original_sentence)
            both_sentences = f"{translated_sentence}\n\n{original_sentence}\n\n"
            self.write_to_file(both_sentences, self.out_path)
            self.write_to_file(str(counter), self.counter_path, mode="w")
        self.quit()

    def set_out_path(self):
        self.out_path = self.ebook.path.replace(
            ".txt", f"_translated_to_{self.target_language}.txt"
        )

    def set_counter_path(self):
        self.counter_path = self.ebook.path.replace(
            ".txt", f"_counter.txt"
        )

    def write_counter_to_file(self, counter):
        self.write_to_file(counter, self.counter_path, mode="w")

    def write_to_file(self, text, path, mode="a"):
        with open(path, mode) as file:
            file.write(text + ' ')

    def read_counter(self):
        with open(self.counter_path) as file:
            return int(file.read())

    def set_start_point(self):
        if os.path.exists(self.counter_path):
            start_point = self.read_counter() + 1
            print(f"Continuing translation from sentence {start_point}")
            self.ebook.sentences = self.ebook.sentences[start_point:]
        else:
            print("Starting translation from the beginning.")

    def quit(self):
        self.translator.quit()


if __name__ == '__main__':
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(THIS_DIR)
    path = os.path.join(ROOT_DIR, "ebooks/harry_potter1_es.txt")
    ebook_translator = EbookTranslator(path, "es", "de", engine="DeepL")
    ebook_translator.translate()
