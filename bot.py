from discord.ext import commands
import discord
import openai

BOT_TOKEN = ""
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

OPENAI_TOKEN = ""
openai.api_key = OPENAI_TOKEN

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def chatgpt(ctx, *, args):
    print("A:\"", args, "\"")
    response = openai.Completion.create(
	    model="text-davinci-003", 
		max_tokens=800,
		temperature=0.5,
        presence_penalty=0,
        frequency_penalty=0,
		best_of=1,
		prompt=args
    )
    await ctx.send(response.choices[0].text)
    print("Q:\"", response.choices[0].text, "\"")

bot.run(BOT_TOKEN)
