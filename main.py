import os
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ ซิงก์คำสั่งเรียบร้อยแล้ว {len(synced)} คำสั่ง")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการซิงก์คำสั่ง: {e}")
    print(f"✅ บอทออนไลน์แล้วในชื่อ: {bot.user}")

@bot.tree.command(name="join", description="สั่งให้บอทเข้าห้องเสียง")
@app_commands.describe(channel="เลือกห้องเสียง")
async def join(interaction: discord.Interaction, channel: discord.VoiceChannel = None):
    await interaction.response.defer()
    target_channel = channel or (interaction.user.voice.channel if interaction.user.voice else None)

    if target_channel:
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(target_channel)
        else:
            await target_channel.connect()
        await interaction.followup.send(f"🔊 เข้าห้อง **{target_channel.name}** เรียบร้อยแล้ว!")
    else:
        await interaction.followup.send("❌ กรุณาระบุห้องเสียง หรือเข้าไปอยู่ในห้องเสียงก่อนครับ!", ephemeral=True)

@bot.tree.command(name="leave", description="สั่งให้ออกจากห้องเสียง")
async def leave(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.followup.send("👋 ออกจากห้องเสียงเรียบร้อยแล้ว!")
    else:
        await interaction.followup.send("❌ บอทไม่ได้อยู่ในห้องเสียงครับ", ephemeral=True)

TOKEN = os.getenv('BOT_TOKEN')
bot.run(TOKEN)
