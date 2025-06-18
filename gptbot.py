import os
from openai import OpenAI
from dotenv import load_dotenv
class GPTBot:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("GPT_TOKEN"))

    def prompt(self,message):
        response = self.client.responses.create(
            model="gpt-4.1",
            input=message,
            max_output_tokens=200,temperature=0.3
        )


        return response.output_text

