import os
import asyncio
from flask import Flask
from threading import Thread
import nextcord
from nextcord.ext import commands

# ==================================================
# 1. ระบบ Keep-Alive (รันแบบ Background ไม่บล็อก Discord Bot)
# ==================================================
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    # กำหนด debug=False และ use_reloader=False เพื่อไม่ให้ Flask ดักจับ Process หลัก
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# เรียกใช้งาน Web Server ใน Background Thread
keep_alive()

# ==================================================
# 2. ตั้งค่า Discord Bot
# ==================================================
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ เข้าสู่ระบบสำเร็จ: {bot.user}")

# ==================================================
# 3. Slash Commands
# ==================================================

@bot.slash_command(
    name="join",
    description="ให้บอทเข้าห้องเสียงที่เลือก"
)
async def join(
    interaction: nextcord.Interaction,
    channel: nextcord.VoiceChannel
):
    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ ใช้คำสั่งนี้ในเซิร์ฟเวอร์เท่านั้น", 
            ephemeral=True
        )

    await interaction.response.defer()

    try:
        voice = interaction.guild.voice_client

        # เคลียร์ Connection เก่าเพื่อป้องกัน Socket ค้าง
        if voice:
            try:
                await voice.disconnect(force=True)
                await asyncio.sleep(1)
            except Exception:
                pass

        # เชื่อมต่อใหม่พร้อมตั้งค่า reconnect และ timeout
        vc = await channel.connect(reconnect=True, timeout=60.0)
        
        # ปรับสถานะ Deafen บอท เพื่อลด UDP Traffic ที่โดน Discord ตัดสาย
        await interaction.guild.change_voice_state(channel=channel, self_deaf=True)

        await interaction.followup.send(
            f"✅ บอทเข้าห้อง {channel.mention} เรียบร้อยแล้ว"
        )

    except Exception as e:
        await interaction.followup.send(
            f"❌ เกิดข้อผิดพลาดในการเข้าห้องเสียง: `{e}`"
        )


@bot.slash_command(
    name="leave",
    description="ให้บอทออกจากห้องเสียง"
)
async def leave(interaction: nextcord.Interaction):
    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ ใช้คำสั่งนี้ในเซิร์ฟเวอร์เท่านั้น", 
            ephemeral=True
        )

    voice = interaction.guild.voice_client

    if not voice:
        return await interaction.response.send_message(
            "❌ บอทไม่ได้อยู่ในห้องเสียง"
        )

    await voice.disconnect(force=True)
    await interaction.response.send_message(
        "✅ บอทออกจากห้องเสียงแล้ว"
    )

# ==================================================
# 4. รันบอท
# ==================================================
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("ไม่พบ DISCORD_TOKEN ใน Environment Variables")

bot.run(TOKEN)
