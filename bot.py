import discord
from discord.ext import commands
import re
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for X links"))
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    def clean_link(match):
        url = match.group()
        clean_url = re.sub(r'\?.*', '', url)
        return clean_url.replace("twitter.com", "fxtwitter.com").replace("x.com", "fxtwitter.com")
    
    new_content = re.sub(r'https?://(www\.)?(x\.com|twitter\.com)/[^\s]+', clean_link, message.content)
    
    if new_content != message.content:
        webhook = await get_webhook(message.channel)
        sent_message = await webhook.send(
            content=new_content,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url if message.author.avatar else None,
            wait=True
        )
        
        await message.delete()
        
        bot.message_cache[sent_message.id] = message.author.id
    
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message = reaction.message
    if message.id in bot.message_cache and bot.message_cache[message.id] == user.id:
        if reaction.emoji == "❌":
            await message.delete()
            del bot.message_cache[message.id]

async def get_webhook(channel):
    try:
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            if webhook.user.id == bot.user.id:
                return webhook
        return await channel.create_webhook(name="URL Rewriter")
    except discord.HTTPException as e:
        print(f"Failed to create webhook: {e}")
        return None

bot.message_cache = {}

bot.run(TOKEN)
