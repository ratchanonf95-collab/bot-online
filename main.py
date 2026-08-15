import os
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ ซิงก์คำสั่งเรียบร้อยแล้วทั้งหมด {len(synced)} คำสั่ง")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการซิงก์คำสั่ง: {e}")
    print(f"✅ บอทออนไลน์แล้วในชื่อ: {bot.user}")


# 1. คำสั่ง /join - สามารถเลือกห้องเสียงที่ต้องการได้
@bot.tree.command(
    name="join", 
    description="สั่งให้บอทเข้าห้องเสียง (เลือกระบุห้อง หรือไม่ระบุเพื่อเข้าห้องที่คุณอยู่)"
)
@app_commands.describe(channel="เลือกห้องเสียงที่ต้องการให้บอทเข้าไป")
async def join(interaction: discord.Interaction, channel: discord.VoiceChannel = None):
    # ถ้าผู้ใช้ระบุช่องมา ให้ใช้ช่องนั้น ถ้าไม่ระบุ ให้ใช้ช่องที่ผู้ใช้อยู่ปัจจุบัน
    target_channel = channel or (interaction.user.voice.channel if interaction.user.voice else None)

    if target_channel:
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(target_channel)
        else:
            await target_channel.connect()
        await interaction.response.send_message(
            f"🔊 เข้าห้อง **{target_channel.name}** เรียบร้อยแล้วครับ!"
        )
    else:
        await interaction.response.send_message(
            "❌ กรุณาระบุห้องเสียง หรือเข้าไปอยู่ในห้องเสียงก่อนใช้คำสั่งครับ!", ephemeral=True
        )


# 2. คำสั่ง /leave - สั่งให้ออกจากห้อง
@bot.tree.command(name="leave", description="สั่งให้บอทออกจากห้องเสียง")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("👋 ออกจากห้องเสียงเรียบร้อยแล้ว!")
    else:
        await interaction.response.send_message(
            "❌ บอทไม่ได้อยู่ในห้องเสียงครับ", ephemeral=True
        )


TOKEN = os.getenv('BOT_TOKEN')
bot.run(TOKEN)
