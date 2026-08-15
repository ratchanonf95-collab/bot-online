import discord
from discord import app_commands
from discord.ext import commands

# 🆔 ใส่ ID ของห้องเสียงที่ต้องการให้ออนประจำ (ถ้ามี)
VOICE_CHANNEL_ID =

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  # ซิงก์คำสั่ง Slash Commands ไปที่ Discord
  try:
    synced = await bot.tree.sync()
    print(f"✅ ซิงก์คำสั่งเรียบร้อยแล้วทั้งหมด {len(synced)} คำสั่ง")
  except Exception as e:
    print(f"❌ เกิดข้อผิดพลาดในการซิงก์คำสั่ง: {e}")

  print(f"✅ บอทออนไลน์แล้วในชื่อ: {bot.user}")


# 1. คำสั่ง Slash Command: /join (กดผ่านโปรไฟล์ได้)
@bot.tree.command(
    name="join", description="สั่งให้บอทเข้ามาในห้องเสียงที่คุณอยู่"
)
async def join(interaction: discord.Interaction):
  if interaction.user.voice:
    channel = interaction.user.voice.channel
    if interaction.guild.voice_client:
      await interaction.guild.voice_client.move_to(channel)
    else:
      await channel.connect()
    await interaction.response.send_message(
        f"🔊 เข้าห้อง **{channel.name}** เรียบร้อยแล้วครับ!"
    )
  else:
    await interaction.response.send_message(
        "❌ คุณต้องเข้าไปอยู่ในห้องเสียงก่อนสั่งครับ!", ephemeral=True
    )


# 2. คำสั่ง Slash Command: /leave (กดผ่านโปรไฟล์ได้)
@bot.tree.command(name="leave", description="สั่งให้บอทออกจากห้องเสียง")
async def leave(interaction: discord.Interaction):
  if interaction.guild.voice_client:
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("👋 ออกจากห้องเสียงเรียบร้อยแล้ว!")
  else:
    await interaction.response.send_message(
        "❌ บอทไม่ได้อยู่ในห้องเสียงครับ", ephemeral=True
    )


# ⚠️ นำ Token ใหม่ของคุณมาวางตรงนี้
bot.run("BOT_TOKEN")
