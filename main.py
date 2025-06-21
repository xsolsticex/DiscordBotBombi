import asyncio
from datetime import datetime
import os
from zoneinfo import ZoneInfo
import discord
from discord import Attachment, Colour, Embed, Message,DMChannel
from discord.ext import commands,tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
from datetime import datetime, timedelta
from AdviceAPI import AdviceAPI
from BotTranslator import BotTranslator
from ConfirmViews import ConfirmView
from constants import Servers,SPAIN
from gptbot import GPTBot


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents,command_prefix="!")
guilds = {}
lista = []
usuarios = set()

gpt = GPTBot()
translator = BotTranslator()
advicer = AdviceAPI()

documentos = 0

load_dotenv()

@client.event
async def on_ready():
    send_advice.start()
    channels = client.guilds
    for element in channels:
        lista.append({f"{element.name}":f"{element.id}"})
    guilds["servers"] = lista


@client.event
async def on_message(message:Message):
    
    if message.author == client.user:
        return
    channel = message.channel
    usuario = message.author
    if isinstance(channel,DMChannel):
        if message.attachments:
            view = ConfirmView()
            file : Attachment = message.attachments[0]
            if file.filename.endswith((".mp3",".ogg")):
                await usuario.send("Quieres enviar este audio?",view=view)
                await view.wait()

                if view.value is True:
                    now = datetime.now(SPAIN)
                    
                    channel = client.get_channel(Servers.SALUD_MENTAL.value)
                    file = await file.to_file(filename=f"Testimonio - {now.date()}.ogg")
    
                    await channel.send(file=file)
                    await usuario.send("Has enviado el audio")
                else:
                    await usuario.send("Has cancelado el audio")
            else:
                print("Archivo no valido")
        else:
            print("No hay datos adjuntos")

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
        channel = client.get_channel(Servers.BIBLIOTEK.value)
        if mensaje:
            respuesta = await gpt.prompt(user.name,text)
            await channel.send(respuesta)

@tasks.loop(hours=24)
async def send_advice():
    channel = client.get_channel(Servers.HIPI_TESTS.value)

    advice,author = advicer.get_advice()

    if advice and author:
        translated = translator.translate(advice)
        embed_message  = Embed(
        color=Colour.blue(),
        description=translated,
        title="Frase Zen del Dia",

        )
        embed_message.set_author(name=author)
        embed_message.set_image(url="https://www.lavanguardia.com/files/og_thumbnail/uploads/2021/02/16/602bb71429cff.jpeg")
        await channel.send(embed=embed_message)

@send_advice.before_loop
async def before_send_advice():
    await client.wait_until_ready()
    now = datetime.now(SPAIN)
    target = now.replace(hour=8, minute=0, second=0, microsecond=0)

    if now > target:
        target += timedelta(days=1)

    wait_seconds = (target - now).total_seconds()
    await asyncio.sleep(wait_seconds)

@client.command()
async def advice(ctx: Context):
    await send_advice()
    
@client.command()
async def post(ctx: Context, *, text = None):
    usuario = ctx.author
    current_channel = ctx.channel
    message = ctx.message

    if not text:
        await message.delete()
        await usuario.send("❌ Debes escribir un mensaje. Usa `!post <tu mensaje>` por DM.")
        return
    
    try:
        if isinstance(current_channel,DMChannel):
            channel = client.get_channel(Servers.SALUD_MENTAL.value)
            fecha = datetime.now(SPAIN)
            msg_embed = Embed(
                title=f"Testimonio Anónimo - {fecha.date()}",
                description=text,
                colour=Colour.brand_green()
            )
            msg_embed.set_image(url="https://sorece.org/wp-content/uploads/2024/01/sorece-blog-por-que-es-importante-hablar-de-la-salud-mental-1024x683.webp")

            await channel.send(embed=msg_embed)
            await usuario.send("Tu mensaje fue publicado de forma anónima.")
        else:
            await message.delete()
            await current_channel.send("Uso de comando !post -> Envia `!post <tu mensaje>`, no en canales públicos")

    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        try:
            await usuario.send("Ocurrió un error al publicar tu mensaje. Intenta más tarde.")
        except Exception as e:
            print(e)



client.run(os.getenv("TOKEN"))