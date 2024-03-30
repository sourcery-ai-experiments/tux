import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    group = app_commands.Group(name="roles", description="Role commands.")

    @group.command(name="toggle", description="Toggles a role for the member.")
    async def toggle(
        self, interaction: discord.Interaction, member: discord.Member, role: discord.Role
    ) -> None:
        if role in member.roles:
            await member.remove_roles(role)
            logger.info(f"{member} removed {role} by {interaction.user}")
            await interaction.response.send_message(f"Removed {role} from {member}.")
        else:
            await member.add_roles(role)
            logger.info(f"{member} added {role} by {interaction.user}")
            await interaction.response.send_message(f"Added {role} to {member}.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Roles(bot))
