import discord
import os
import requests
import json
import random

client = discord.Client()

sad = ["sad", "unhappy", 'depressed', 'mad', 'angry', 'kys', 'unlucky', 'unlucko', 'sadge', 'smoge']

encourage = [
  "Hang in there pal!",
  "You'll get'em next time :)",
  "Do not fret, you are the best!",
  "You are a great person/bot!",
  "Do not worry, I still love you"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)

@client.event
async def on_ready() :
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('!hello'):
    await message.channel.send('Hello there!')

  if any(word in message.content for word in sad):
    await message.channel.send(random.choice(encourage))

client.run(os.getenv('TOKEN'))