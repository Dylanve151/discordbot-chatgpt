import os
import threading
import random
import asyncio
import requests
import tempfile

import discord
from openai import OpenAI
from discord.ext import commands
from dotenv import load_dotenv


## .env variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_ADMIN_NAMES = os.getenv('DISCORD_ADMIN_NAMES').split(',')
DISCORD_ALL_USE = os.getenv('DISCORD_ALL_USE')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_TXT_MODEL = os.getenv('OPENAI_TXT_MODEL')
OPENAI_TXT_TEMPERATTURE = float(os.getenv('OPENAI_TXT_TEMPERATTURE'))
OPENAI_TTS_MODEL = os.getenv('OPENAI_TTS_MODEL')
OPENAI_TTS_SPEED = float(os.getenv('OPENAI_TTS_SPEED'))
OPENAI_TTS_VOICE = os.getenv('OPENAI_TTS_VOICE')
OPENAI_IMG_MODEL = os.getenv('OPENAI_IMG_MODEL')
OPENAI_IMG_SIZE = os.getenv('OPENAI_IMG_SIZE')
OPENAI_IMG_QUALITY = os.getenv('OPENAI_IMG_QUALITY')

if DISCORD_ALL_USE.upper() == 'TRUE':
    DISCORD_ALL_USE = True
else:
    DISCORD_ALL_USE = False


## discord config/variables
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


## OpenAI config/variables
client = OpenAI()
OPENAI_TTS_VOICES = ["alloy","echo","fable","onyx","nova","shimmer"]


## variables
if True:
        ffmpeg_exe = 'ffmpeg/bin/ffmpeg.exe'
else:
        ffmpeg_exe = 'ffmpeg'


## Function
async def openai_gentxt(chatmsg, question):
        print("TEXT Q:\""+str(question)+"\"")
        response = client.chat.completions.create(
                model=OPENAI_TXT_MODEL,
                max_tokens=800,
                temperature=OPENAI_TXT_TEMPERATTURE,
                n=1,
                messages=[{"role": "user", "content": question}]
        )
        embed = discord.Embed(title=question, description=response.choices[0].message.content)
        await chatmsg.reply(embed=embed)
        print("TEXT A:\""+str(response.choices[0].message.content)+"\"")


async def openai_gentts(chatmsg, question, OPENAI_TTS_VOICE=None):
        if chatmsg.message.author.voice != None:
                if OPENAI_TTS_VOICE == None:
                        OPENAI_TTS_VOICE = random.choice(OPENAI_TTS_VOICES)
                print("TTS Q:\""+str(question)+"\"")
                tFile = tempfile.NamedTemporaryFile(suffix='.mp3')
                response = client.audio.speech.create(
                        model=OPENAI_TTS_MODEL,
                        voice=OPENAI_TTS_VOICE,
                        response_format="mp3",
                        speed=OPENAI_TTS_SPEED,
                        input=question
                )
                response.stream_to_file(tFile.name)
                channel = chatmsg.message.author.voice.channel
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(tFile.name, executable=ffmpeg_exe))
                while not vc.is_playing():
                        await asyncio.sleep(0.5)
                while vc.is_playing():
                        await asyncio.sleep(0.5)
                await vc.disconnect()
                tFile.close()
                print("TTS A:\""+"done"+"\"")


async def openai_genimage(chatmsg, question):
        print("IMG Q:\""+str(question)+"\"")
        tFile = tempfile.NamedTemporaryFile(suffix='.png')
        response = client.images.generate(
                model=OPENAI_IMG_MODEL,
                size=OPENAI_IMG_SIZE,
                quality=OPENAI_IMG_QUALITY,
                n=1,
                prompt=question
        )
        r = requests.get(response.data[0].url, allow_redirects=True)
        tFile.write(r.content)
        tFile.flush()
        await chatmsg.reply(file=discord.File(tFile.name))
        tFile.close()
        print("IMG A:\""+str(response.data[0].url)+"\"")


@bot.event
async def on_ready():
        print(f'We have logged in as {bot.user}')


@bot.command()
async def chatgpt(ctx, *, args):
        if DISCORD_ALL_USE or ctx.author.name in DISCORD_ADMIN_NAMES:
            thread = threading.Thread(target=await openai_gentxt(ctx, args))
            thread.start()
        else:
            print('nope')


@bot.command()
async def chatgpt_tts(ctx, *, args):
        if DISCORD_ALL_USE or ctx.author.name in DISCORD_ADMIN_NAMES:
                thread = threading.Thread(target=await openai_gentts(ctx, args, OPENAI_TTS_VOICE))
                thread.start()
        else:
            print('nope')


@bot.command()
async def chatgpt_image(ctx, *, args):
        if DISCORD_ALL_USE or ctx.author.name in DISCORD_ADMIN_NAMES:
                thread = threading.Thread(target=await openai_genimage(ctx, args))
                thread.start()
        else:
            print('nope')


bot.run(DISCORD_BOT_TOKEN)
