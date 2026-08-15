import os
import asyncio
import nextcord
from nextcord.ext import commands
import yt_dlp

# ==================================================
# 1. ตั้งค่า Discord Bot & Intents
# ==================================================
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

# ตั้งค่า yt-dlp และ FFmpeg Options
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

@bot.event
async def on_ready():
    print(f"✅ บอทพร้อมใช้งานแล้ว: {bot.user}")

# ==================================================
# 2. Slash Commands
# ==================================================

@bot.slash_command(name="play", description="เล่นเพลงจาก YouTube (ใส่ลิงก์หรือชื่อเพลง)")
async def play(
    interaction: nextcord.Interaction, 
    query: str
):
    if interaction.guild is None:
        return await interaction.response.send_message("❌ ใช้ในเซิร์ฟเวอร์เท่านั้น", ephemeral=True)

    # ดึง Voice Channel ของผู้ใช้
    user_voice = interaction.user.voice
    if not user_voice or not user_voice.channel:
        return await interaction.response.send_message("❌ คุณต้องเข้าห้องเสียงก่อนสั่งเล่นเพลง", ephemeral=True)

    await interaction.response.defer()

    try:
        voice = interaction.guild.voice_client

        # ย้ายเข้าห้องเสียงหากยังไม่ได้เข้า หรืออยู่อื่นห้อง
        if not voice:
            voice = await user_voice.channel.connect(reconnect=True, timeout=60.0)
            await interaction.guild.change_voice_state(channel=user_voice.channel, self_deaf=True)
        elif voice.channel != user_voice.channel:
            await voice.move_to(user_voice.channel)

        # ค้นหาและดึง URL เพลงจาก YouTube
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            audio_url = info['url']
            title = info.get('title', 'เพลงไม่ทราบชื่อ')

        # หยุดเพลงเดิมถ้ากำลังเล่นอยู่
        if voice.is_playing():
            voice.stop()

        # เล่นเพลงผ่าน FFmpeg
        source = nextcord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
        voice.play(source)

        await interaction.followup.send(f"🎵 กำลังเล่น: **{title}**")

    except Exception as e:
        await interaction.followup.send(f"❌ เกิดข้อผิดพลาด: `{e}`")


@bot.slash_command(name="stop", description="หยุดเล่นเพลงและออกจากห้องเสียง")
async def stop(interaction: nextcord.Interaction):
    voice = interaction.guild.voice_client
    if not voice:
        return await interaction.response.send_message("❌ บอทไม่ได้อยู่ในห้องเสียง", ephemeral=True)

    if voice.is_playing():
        voice.stop()
    await voice.disconnect(force=True)
    await interaction.response.send_message("⏹️ หยุดเล่นเพลงและออกจากห้องเสียงแล้ว")

# ==================================================
# 3. รันบอท
# ==================================================
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("ไม่พบ DISCORD_TOKEN ใน Environment Variables")

bot.run(TOKEN)
