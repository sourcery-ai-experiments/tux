import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from tux.utils.embeds import create_success_embed


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Checks the bot's latency.")
    async def ping(self, interaction: discord.Interaction) -> None:
        discord_ping = round(self.bot.latency * 1000)

        embed = create_success_embed(
            interaction=interaction,
            title="Pong!",
            description=f"Discord Websocket Latency: `{discord_ping}ms`",
        )

        logger.info(f"{interaction.user} used the ping command in {interaction.channel}.")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
