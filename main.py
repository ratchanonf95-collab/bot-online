import os
import discord
from discord.ext import commands

# เปิดใช้งาน Intents พื้นฐาน
intents = discord.Intents.default()
intents.message_content = True  # เปิดรับข้อความ

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'บอทออนไลน์แล้วในชื่อ: {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# ดึง Token จาก Environment Variable (หรือใส่ Token ตรงๆ ในเครื่องหมายอัญประกาศได้)
TOKEN = os.getenv('BOT_TOKEN')
bot.run(TOKEN)
