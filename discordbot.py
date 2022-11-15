import discord
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
from roast_handler import decide_roast

# ==========================================
# Just a basic discord bot to have fun with.
# ==========================================

TOKEN = 'YOUR TOKEN HERE'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    
    channel = str(message.channel.name)

    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'ai-roaster':
        ai_response, ai_score = decide_roast(user_message)
        readable_socre = round((float(ai_score)) * 100)

        await message.channel.send(f"{ai_response} : {readable_socre}%")
        return


client.run(TOKEN)