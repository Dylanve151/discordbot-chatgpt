import os
import threading
from pathlib import Path
import random
import nacl
import ffmpeg
import asyncio

import discord
from openai import OpenAI
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
os.environ['OPENAI_API_KEY'] = OPENAI_TOKEN

OPENAI_MODEL = os.getenv('OPENAI_MODEL')

OPENAI_TTS_VOICES = ["alloy","echo","fable","onyx","nova","shimmer"]


client = OpenAI()

async def chatgpt_gentxt_old(chatmsg, question):
        print("Q:\"", question, "\"")
        response = client.completions.create(
                model=OPENAI_MODEL,
                max_tokens=800,
                temperature=0.5,
                presence_penalty=0,
                frequency_penalty=0,
                best_of=1,
                prompt=question
        )
        embed = discord.Embed(title=question, description=response.choices[0].text)
        await chatmsg.reply(embed=embed)
        print("A:\"", response.choices[0].text, "\"")


async def chatgpt_gentxt(chatmsg, question):
        print("Q:\"", question, "\"")
        response = client.chat.completions.create(
                model=OPENAI_MODEL,
                max_tokens=800,
                temperature=0.5,
                n=1,
                messages=[{"role": "user", "content": question}]
        )
        embed = discord.Embed(title=question, description=response.choices[0].message.content)
        await chatmsg.reply(embed=embed)
        print("A:\"", response.choices[0].message.content, "\"")


async def chatgpt_gentts(chatmsg, question):
        if chatmsg.message.author.voice != None:
                print("TTS this:\"", question, "\"")
                response = client.audio.speech.create(
                        model="tts-1",
                        voice=random.choice(OPENAI_TTS_VOICES),
                        response_format="mp3",
                        speed=1.0,
                        input=question
                )
                response.stream_to_file("/tmp/tts.mp3")
                channel = chatmsg.message.author.voice.channel
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio("/tmp/tts.mp3", executable='ffmpeg'))
                while not vc.is_playing():
                        await asyncio.sleep(0.5)
                while vc.is_playing():
                        await asyncio.sleep(0.5)
                await vc.disconnect()


@bot.event
async def on_ready():
        print(f'We have logged in as {bot.user}')


@bot.command()
async def chatgpt(ctx, *, args):
        thread = threading.Thread(target=await chatgpt_gentxt(ctx, args))
        thread.start()


@bot.command()
async def chatgpt_tts(ctx, *, args):
        thread = threading.Thread(target=await chatgpt_gentts(ctx, args))
        thread.start()


@bot.command()
async def chatgpt_test(ctx, *, args):
        if ctx.message.author.voice != None:
                print(ctx.message.author.voice.channel)
        embed = discord.Embed(title='test', description='ook test')
        await ctx.reply(embed=embed)



bot.run(BOT_TOKEN)
