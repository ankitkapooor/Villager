from transformers import AutoModelForCausalLM, AutoTokenizer
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from model_generator import Generator

#model and tokenizer initialization through HuggingFace

#tokenizer = AutoTokenizer.from_pretrained('Models/epochs_4/')
#model = AutoModelForCausalLM.from_pretrained('Models/epochs_4/')

tokenizer = AutoTokenizer.from_pretrained('Models/20K_steps/')
model = AutoModelForCausalLM.from_pretrained('Models/20K_steps/')
special_token = '<|endoftext|>'

#Creating a discord bot
client = commands.Bot(command_prefix = '!', help_command = None)

#command executed when the bot first comes online
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The world // !help"))

#the first message sent by MinecraftLibrarian when it joins a server
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            title = "Hello, there!"
            description = "I am a Minecraft Villager, and I've just been invited to join this server. Type **!help** to understand more about what I can do 🦾"
            emb = discord.Embed(title = title, description = description, color = 0xf4fc58)
            await channel.send(embed = emb)
        break

#constantly runs, takes messages from the user and responds using the provided dataset
@client.event
async def on_message(message):
    msg = message.content.strip()
    reply = Generator.get_reply(msg.strip())
    if message.author == client.user:
        return

    if message.content.startswith(msg) and not message.content.startswith('!'):
        await message.channel.send(reply)
    await client.process_commands(message)

    #a log of every conversation is recorded on Logs.txt
    with open('Logs.txt', 'a', encoding = "UTF-8") as f:
        f.write(f'User: {msg}\nVillager#9524: {reply}\n')

#help command: type "!help" to get more information about the bot
@client.command()
async def help(ctx, *, message = "all"):
    name = "I am a Minecraft Villager!"
    text = 'I am a Natural Language Generation ChatBot coded using a distilled version of GPT-2 from the Huggingface repository. I am capable of holding any conversaion with you. I have been trained on the Topical-Chat dataset provided by Amazon. I have read over 50,000 back-and-forths and all the things that I say are generated completely by me!'

    emb = discord.Embed(title = name, description = text, color = 0xf4fc58)
    await ctx.send(embed = emb)

client.run('OTQxMjQ2NjMyOTY2NjE5MTQ2.YgTKPA._eMhP_z3ogriFyM91OUAr08HPWA')
