import nextcord
from nextcord.ext import commands

bot = commands.Bot(intents=nextcord.Intents.all())

@bot.slash_command(name="join", description="ให้บอทเข้าช่องเสียง")
async def join(interaction: nextcord.Interaction):

    if not interaction.user.voice:
        return await interaction.response.send_message(
            "❌ คุณต้องอยู่ในช่องเสียงก่อน"
        )

    channel = interaction.user.voice.channel

    if interaction.guild.voice_client:
        await interaction.guild.voice_client.move_to(channel)
    else:
        await channel.connect()

    await interaction.response.send_message(
        f"✅ เข้าช่องเสียง `{channel.name}` แล้ว"
    )


@bot.slash_command(name="leave", description="ให้บอทออกจากช่องเสียง")
async def leave(interaction: nextcord.Interaction):

    voice = interaction.guild.voice_client

    if not voice:
        return await interaction.response.send_message(
            "❌ บอทไม่ได้อยู่ในช่องเสียง"
        )

    await voice.disconnect()

    await interaction.response.send_message(
        "✅ ออกจากช่องเสียงแล้ว"
    )


bot.run("BOT_TOKEN")
