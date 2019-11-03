from text_tokenizer import TextTokenizer


class Ebook:
    def __init__(self, path):
        self.path = path
        self.read()
        self.split_into_sentences()

    def read(self):
        print("Reading text into memory.")
        with open(self.path) as file:
            self.content = file.read()

    def split_into_sentences(self):
        print("Tokenizing text into sentences.")
        self.sentences = TextTokenizer(self.content).tokenize()
