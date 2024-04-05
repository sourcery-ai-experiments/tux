import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger


class Jail(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.has_any_role("Admin", "Sr. Mod", "Mod", "Jr. Mod")
    @app_commands.command(name="jail", description="Strip all roles except the jail role")
    @app_commands.describe(member="Which member to jail", reason="Reason for jail")
    async def jail(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
    ) -> None:
        logger.info(f"{interaction.user} jailed {member.display_name} in {interaction.channel}")

        if interaction.guild:
            jail_role = interaction.guild.get_role(1225848510008524851)
            if jail_role:
                response = await self.execute_jail(
                    interaction=interaction,
                    member=member,
                    jail_role=jail_role,
                    reason=reason or "None provided",
                )

                await interaction.response.send_message(embed=response)

    async def execute_jail(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        jail_role: discord.Role,
        reason: str | None = None,
    ) -> discord.Embed:
        try:
            await member.edit(roles=[jail_role])
            embed = discord.Embed(
                title=f"Jailed {member.display_name}!",
                color=discord.Colour.gold(),
                description=f"Reason: `{reason}`",
            )
            embed.set_footer(
                text=f"Jailed by {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url,
            )

            logger.info(f"Successfully Jailed {member.display_name}.")

        except discord.errors.Forbidden as error:
            embed = discord.Embed(
                title=f"Failed to jail {member.display_name}",
                color=discord.Colour.red(),
                description=f"Insufficient permissions. Error Info: `{error}`",
            )
            logger.error(f"Failed to jail {member.display_name}. Error: {error}")

        return embed


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Jail(bot))
