import requests
from translate import Translator

from BotTranslator import BotTranslator

class AdviceAPI:
    def __init__(self):
        self.url = "https://zenquotes.io/api/today"

    def get_advice(self)-> list:
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            phrase : dict = data[0]
            result = [phrase.get("q"),phrase.get("a")]
            return result

        
translator = BotTranslator()
advice = AdviceAPI()