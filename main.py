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
    # ตรวจสอบว่าเป็นเซิร์ฟเวอร์
    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ คำสั่งนี้ใช้ในเซิร์ฟเวอร์เท่านั้น"
        )

    # เช็กสิทธิ์ของบอท
    permissions = channel.permissions_for(interaction.guild.me)

    if not permissions.connect:
        return await interaction.response.send_message(
            f"❌ บอทไม่มีสิทธิ์เข้า {channel.mention}"
        )

    await interaction.response.defer()

    try:
        voice = interaction.guild.voice_client

        if voice:
            await voice.move_to(channel)
        else:
            await channel.connect()

        await interaction.followup.send(
            f"✅ เข้า {channel.mention} แล้ว"
        )

    except Exception as e:
        await interaction.followup.send(
            f"❌ เข้าไม่ได้\n`{e}`"
        )


@bot.slash_command(
    name="leave",
    description="ให้บอทออกจากห้องเสียง"
)
async def leave(interaction: nextcord.Interaction):

    voice = interaction.guild.voice_client

    if not voice:
        return await interaction.response.send_message(
            "❌ ตอนนี้บอทไม่ได้อยู่ในห้องเสียง"
        )

    await voice.disconnect()

    await interaction.response.send_message(
        "✅ ออกจากห้องเสียงแล้ว"
    )


bot.run("BOT_TOKEN")
