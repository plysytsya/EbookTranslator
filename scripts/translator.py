import googletrans


class Translator:

    def __init__(self, source_language, target_language, engine="google"):
        self.source_language = source_language
        self.target_language = target_language
        self.set_engine(engine)

    def set_engine(self, name):
        engines = {"google": GoogleEngine(self.source_language, self.target_language)}
        assert name in engines.keys(), f"{name} is not a supported engine."
        self.engine = engines[name]

    def translate(self, text):
        return self.engine.translate(text)


class GoogleEngine:
    """Free google-translate client provided by:
    https://github.com/ssut/py-googletrans """

    def __init__(self, source_language, target_language):
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
