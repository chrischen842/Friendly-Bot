import discord
import os
import requests
import json
import random
from replit import db

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

def update_encourage(encourage_msg):
  if "encouragements" in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encourage_msg)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encourage_msg]

def remove_encourage(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  msg = message.content 

  if message.author == client.user:
    return

  if msg.startswith('!quote'):
    quote = get_quote()
    await message.channel.send(quote)

  options = encourage
  if 'encouragements' in db.keys():
    options = options + list(db['encouragements'])

  if any(word in msg for word in sad):
    await message.channel.send(random.choice(options))

  if msg.startswith('!new'):
    encourage_msg = msg.split('!new ',1)[1]
    update_encourage(encourage_msg)
    await message.channel.send('New encouragement added!')
    
  
  if msg.startswith('!del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('!del',1)[1])
      remove_encourage(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

client.run(os.getenv('TOKEN'))