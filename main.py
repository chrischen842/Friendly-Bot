import discord
import os
import requests
import json
import random
from stayOnline import stayOnline
from replit import db

client = discord.Client()

sad = [
"sad",
"unhappy",
'depressed',
'mad',
'angry',
'kys',
'unlucky',
'unlucko',
'sadge',
'smoge',
':c',
':('
]

encourage = [
  "Hang in there pal!",
  "You'll get'em next time :)",
  "Do not fret, you are the best!",
  "You are a great person/bot!",
  "Do not worry, I still love you!"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)

def update_sad(sad_msg):
  if 'saddb' in db.keys():
    saddb = db['saddb']
    saddb.append(sad_msg)
    db['saddb'] = saddb
  else:
    db['saddb'] = [sad_msg]

def remove_sad(sadindex):
  saddb = db['saddb']
  if len(saddb) > sadindex:
    del saddb[sadindex]
    db['saddb'] = saddb

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
  for k in db.keys():
    print (db[k])


@client.event
async def on_message(message):

  msg = message.content 

  if message.author == client.user:
    return

  if msg.startswith('!quote'):
    quote = get_quote()
    await message.channel.send(quote)

  sadwordbank = sad
  if 'saddb' in db.keys():
    sadwordbank.extend(db["saddb"])

  options = encourage
  if 'encouragements' in db.keys():
    options.extend(db["encouragements"])

  if any(word in msg for word in sadwordbank):
    await message.channel.send(random.choice(options))

  if msg.startswith('!new e'):
    encourage_msg = msg.split('!new e ',1)[1]
    update_encourage(encourage_msg)
    await message.channel.send('New encouragement added!')
  
  if msg.startswith('!new s'):
    sad_msg = msg.split('!new s ',1)[1]
    update_sad(sad_msg)
    await message.channel.send('New sad keyword added!')
    
  if msg.startswith('!remove e'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('!remove e',1)[1])
      remove_encourage(index)
      encouragements = db['encouragements']
    await message.channel.send('Item deleted.')
    await message.channel.send(encouragements)

  if msg.startswith('!remove s'):
    saddb = []
    if 'saddb' in db.keys():
      sadindex = int(msg.split('!remove s',1)[1])
      remove_sad(sadindex)
      saddb = db['saddb']
    await message.channel.send('Item deleted.')
    await message.channel.send(saddb)

  if msg.startswith('!list'):
    encouragements = []
    saddb = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    
    if 'saddb' in db.keys():
      saddb = db['saddb']

    await message.channel.send('Encouragement wordbank:')
    await message.channel.send(encouragements)
    await message.channel.send('Sad wordbank:')
    await message.channel.send(saddb)
  
  if msg.startswith('!turn'):
    value = msg.split('!turn ',1)[1]

    if value.lower() == 'on':
      db['turn'] = True
      await message.channel.send("I am on.")
    elif value.lower() == 'off':
      db['turn'] = False
      await message.channel.send("I am off.")
    else:
      await message.channel.send("Invalid answer.")
  
stayOnline()
client.run(os.getenv('TOKEN'))