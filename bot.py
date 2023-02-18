import os
import asyncio

import discord
import openai
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
openai.api_key = OPENAI_TOKEN

async def respsoneandsent(chatmsg, question):
	print("Q:\"", question, "\"")
	response = openai.Completion.create(
		model="text-davinci-003", 
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
	cmd = respsoneandsent(ctx, args)
	task = asyncio.create_task(cmd)

bot.run(BOT_TOKEN)
