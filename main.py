import asyncio
from datetime import datetime
import os
import discord
from discord import Colour, Embed, Message,DMChannel
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents,command_prefix="!")
guilds = {}
lista = []
usuarios = set()

documentos = 0

load_dotenv()

@client.event
async def on_ready():

    channels = client.guilds
    for element in channels:
      lista.append({f"{element.name}":f"{element.id}"})
    guilds["servers"] = lista


@client.event
async def on_message(message:Message):
      channel = message.channel
      user = message.author
      if isinstance(channel,DMChannel) and not user.bot:
            if user.name not in usuarios:
                  usuarios.add(user.name)
                  await user.send(f"Hola {user.name} en que puedo ayudarte?")
                  await asyncio.sleep(2)
                  await user.send("```Para escribir un post de forma anonima utiliza el comando !post seguido de tu mensaje```")

      await client.process_commands(message)
      #await channel.send(f"Hola {user.name}")
    
@client.command()
async def post(ctx:Context,*,text):
   usuario = ctx.author
   
   channel = client.get_channel(1369649025602814024)
   msg_embed = Embed()
   fecha  = datetime.now()
   msg_embed.title = f"Testimonio Anonimo - {fecha.date()}"
   msg_embed.colour = Colour.brand_green()
   msg_embed.set_image(url="https://sorece.org/wp-content/uploads/2024/01/sorece-blog-por-que-es-importante-hablar-de-la-salud-mental-1024x683.webp")
   msg_embed.description = text
   await channel.send(embed=msg_embed)
   await usuario.send("Mensaje creado")



client.run(os.getenv("TOKEN"))