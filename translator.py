from googletrans import Translator


class TranslatorService:
    def __init__(self, src='en', dest='en'):
        self.translator = Translator()
        self.src = src
        self.dest = dest

    def translate_text(self, text) -> str:
        result = self.translator.translate(text, src=self.src, dest=self.dest)
        return result.text
