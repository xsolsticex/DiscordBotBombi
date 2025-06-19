import asyncio
from datetime import datetime
import os
import discord
from discord import Colour, Embed, Message,DMChannel
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

from gptbot import GPTBot


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents,command_prefix="!")
guilds = {}
lista = []
usuarios = set()

gpt = GPTBot()

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

    await client.process_commands(message)

@client.command()
async def q(ctx:Context,*,text):
    mensaje = text
    canal = ctx.channel
    user = ctx.author
    if isinstance(canal,DMChannel):
        respuesta = await gpt.prompt(user.name,text)
        await user.send(respuesta)
    else:
        channel = client.get_channel(1384845888442335273)
        if mensaje:
            respuesta = await gpt.prompt(user.name,text)
            await channel.send(respuesta)

    
@client.command()
async def post(ctx: Context, *, text):
    usuario = ctx.author
    current_channel = ctx.channel
    try:
        channel = client.get_channel(1382725980887449620)
        fecha = datetime.now()
        msg_embed = Embed(
            title=f"Testimonio Anónimo - {fecha.date()}",
            description=text,
            colour=Colour.brand_green()
        )
        msg_embed.set_image(url="https://sorece.org/wp-content/uploads/2024/01/sorece-blog-por-que-es-importante-hablar-de-la-salud-mental-1024x683.webp")

        await channel.send(embed=msg_embed)
        await usuario.send("Tu mensaje fue publicado de forma anónima.")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        try:
            await usuario.send("Ocurrió un error al publicar tu mensaje. Intenta más tarde.")
        except:
            pass



client.run(os.getenv("TOKEN"))