from nltk.tokenize import sent_tokenize, word_tokenize


class TextTokenizer:
    """Splits text into sentences"""

    def __init__(self, text_as_string):
        self.text = text_as_string

    def tokenize(self, tokens="sentences"):
        assert tokens in ["sentences", "words"]
        if tokens == "sentences":
            return sent_tokenize(self.text)
        elif tokens == "words":
            return word_tokenize(self.text)


if __name__ == '__main__':
    tokenizer = TextTokenizer()
    tokenizer.main()
