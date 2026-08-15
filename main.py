import os
import asyncio
import nextcord
from nextcord.ext import commands, tasks

# ==================================================
# 1. ตั้งค่า Discord Bot
# ==================================================
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ เข้าสู่ระบบสำเร็จ: {bot.user}")
    if not voice_keep_alive.is_running():
        voice_keep_alive.start()

# ==================================================
# 2. ระบบ Voice Keep-Alive (ป้องกันตัดสายทุก 20 วินาที)
# ==================================================
@tasks.loop(seconds=15)
async def voice_keep_alive():
    for guild in bot.guilds:
        if guild.voice_client and guild.voice_client.is_connected():
            try:
                # ส่งสัญญาณ WebSocket Heartbeat ป้องกัน Discord มองว่า Idle
                await guild.voice_client.ws.send_ping()
            except Exception:
                pass

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

        if voice:
            try:
                await voice.disconnect(force=True)
                await asyncio.sleep(1)
            except Exception:
                pass

        # เชื่อมต่อแบบ Reconnect + Timeout 60s
        vc = await channel.connect(reconnect=True, timeout=60.0)
        
        # ตั้งค่า Deafen ช่วยลดการรับส่ง Volume Data
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
