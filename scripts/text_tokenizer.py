

class TextTokenizer:
    """Splits text into sentences"""

    def __init__(self, text_as_string):
        self.text = text_as_string
        self.separators = ['...', '.', '!' '?', ';']

    def tokenize(self):
        pass


if __name__ == '__main__':
    tokenizer = TextTokenizer()
    tokenizer.main()
