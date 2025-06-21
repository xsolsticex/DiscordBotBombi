from translate import Translator


class BotTranslator:
    def __init__(self,to_lang="es"):
        self.to_lang = to_lang
        self.translator = Translator(from_lang="en",to_lang="es",base_url="https://translate.astian.org/",secret_access_key=None)

    
    def translate(self,phrase : str)->str:
        return self.translator.translate(phrase)
    