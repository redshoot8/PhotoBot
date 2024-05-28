from translate import Translator


class TranslatorService:
    def __init__(self, to_lang="en", from_lang="en"):
        self.translator = Translator(to_lang=to_lang, from_lang=from_lang)

    def translate_text(self, text):
        return self.translator.translate(text)
