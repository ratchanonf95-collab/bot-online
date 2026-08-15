import os
import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.all()

bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"เข้าสู่ระบบแล้ว: {bot.user}")


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
            "❌ ใช้คำสั่งนี้ในเซิร์ฟเวอร์เท่านั้น"
        )

    await interaction.response.defer()

    try:
        voice = interaction.guild.voice_client

        if voice:
            await voice.move_to(channel)
        else:
            await channel.connect()

        await interaction.followup.send(
            f"✅ บอทเข้าห้อง {channel.mention} แล้ว"
        )

    except Exception as e:
        await interaction.followup.send(
            f"❌ เกิดข้อผิดพลาด: `{e}`"
        )


@bot.slash_command(
    name="leave",
    description="ให้บอทออกจากห้องเสียง"
)
async def leave(interaction: nextcord.Interaction):

    voice = interaction.guild.voice_client

    if not voice:
        return await interaction.response.send_message(
            "❌ บอทไม่ได้อยู่ในห้องเสียง"
        )

    await voice.disconnect()

    await interaction.response.send_message(
        "✅ บอทออกจากห้องเสียงแล้ว"
    )


TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("ไม่พบ DISCORD_TOKEN ใน Environment Variables")

bot.run(TOKEN)
