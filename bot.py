import os
import threading

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
OpenAI.api_key = OPENAI_TOKEN

OPENAI_MODEL = os.getenv('OPENAI_MODEL')

async def respsoneandsent(chatmsg, question):
	print("Q:\"", question, "\"")
	response = OpenAI.chat.completions.create(
		model=OPENAI_MODEL, 
		max_tokens=800,
		temperature=0.5,
		presence_penalty=0,
		frequency_penalty=0,
		best_of=1,
		prompt=question
	)
	embed = discord.Embed(title=question, description=response["choices"][0]["text"])
	await chatmsg.reply(embed=embed)
	print("A:\"", response.choices[0].text, "\"")

@bot.event
async def on_ready():
	print(f'We have logged in as {bot.user}')

@bot.command()
async def chatgpt(ctx, *, args):
	thread = threading.Thread(target=await respsoneandsent(ctx, args))
	thread.start()

@bot.command()
async def chatgpt_test(ctx, *, args):
        embed = discord.Embed(title='test', description='ook test')
        await ctx.reply(embed=embed)

bot.run(BOT_TOKEN)
