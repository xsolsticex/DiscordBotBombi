import asyncio
import os
from openai import OpenAI
from dotenv import load_dotenv

historial = {}
class GPTBot:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("GPT_TOKEN"))

    async def prompt(self,user,message):
        if user not in historial:
            historial[user] = []

        hist: list = historial[user]
        hist.append({"role":"user","content":message})

        response  = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=hist,
            max_tokens=200,
            temperature=0.3
        )
        #print(response)
        content = response.choices[0].message.content
        print(content)
        hist.append({"role":"assistant","content":content})
        return content






