import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger


class Nick(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.has_any_role("Admin", "Sr. Mod", "Mod", "Jr. Mod")
    @app_commands.command(name="nick", description="Changes nickname for a member")
    @app_commands.describe(
        member="Member to change nickname",
        new_nickname="new nickname",
    )
    async def nick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        new_nickname: str,
    ) -> None:
        logger.info(
            f"{interaction.user} changed nickname for {member.display_name} in {interaction.channel}"
        )

        response = await self.execute_change_nick(
            interaction,
            member,
            new_nickname,
        )

        await interaction.response.send_message(embed=response)

    async def execute_change_nick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        new_nickname: str,
    ) -> discord.Embed:
        try:
            await member.edit(nick=new_nickname)
            embed = discord.Embed(
                title=f"Changed nickname for {member.display_name}!",
                color=discord.Colour.green(),
                description=f"New nickname: `{new_nickname}`",
            )
            embed.set_footer(
                text=f"changed by {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url,
            )

            logger.info(f"Successfully changed nickname for {member.display_name}.")

        except discord.errors.Forbidden as error:
            embed = discord.Embed(
                title=f"Failed to change nickname for {member.display_name}",
                color=discord.Colour.red(),
                description=f"Insufficient permissions. Error Info: `{error}`",
            )
            logger.error(f"Failed to nick {member.display_name}. Error: {error}")

        return embed


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Nick(bot))
