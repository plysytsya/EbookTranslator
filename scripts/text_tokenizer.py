from nltk.tokenize import sent_tokenize


class TextTokenizer:
    """Splits text into sentences"""

    def __init__(self, text_as_string):
        self.text = text_as_string

    def tokenize(self):
        return sent_tokenize(self.text)


if __name__ == '__main__':
    tokenizer = TextTokenizer()
    tokenizer.main()
