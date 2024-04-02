import traceback

import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from tux.utils.constants import Constants as CONST

# Custom error handling mappings and messages.
error_map = {
    # app_commands
    app_commands.AppCommandError: "An error occurred: {error}",
    app_commands.CommandInvokeError: "A command invoke error occurred: {error}",
    app_commands.TransformerError: "A transformer error occurred: {error}",
    app_commands.MissingRole: "You are missing the role required to use this command.",
    app_commands.MissingAnyRole: "You are missing some roles required to use this command.",
    app_commands.MissingPermissions: "You are missing the required permissions to use this command.",
    app_commands.CheckFailure: "You are not allowed to use this command.",
    app_commands.CommandNotFound: "This command was not found.",
    app_commands.CommandOnCooldown: "This command is on cooldown. Try again in {error.retry_after:.2f} seconds.",
    app_commands.BotMissingPermissions: "The bot is missing the required permissions to use this command.",
    app_commands.CommandSignatureMismatch: "The command signature does not match: {error}",
    # commands
    commands.CommandError: "An error occurred: {error}",
    commands.CommandInvokeError: "A command invoke error occurred: {error}",
    commands.ConversionError: "An error occurred during conversion: {error}",
    commands.MissingRole: "You are missing the role required to use this command.",
    commands.MissingAnyRole: "You are missing some roles required to use this command.",
    commands.MissingPermissions: "You are missing the required permissions to use this command.",
    commands.CheckFailure: "You are not allowed to use this command.",
    commands.CommandNotFound: "This command was not found.",
    commands.CommandOnCooldown: "This command is on cooldown. Try again in {error.retry_after:.2f} seconds.",
    commands.BadArgument: "Invalid argument passed. Correct usage:\n```{ctx.command.usage}```",
    commands.MissingRequiredArgument: "Missing required argument. Correct usage:\n```{ctx.command.usage}```",
    commands.MissingRequiredAttachment: "Missing required attachment.",
    commands.NotOwner: "You are not the owner of this bot.",
    commands.BotMissingPermissions: "The bot is missing the required permissions to use this command.",
}


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.error_message = "An error occurred. Please try again later."
        bot.tree.error(
            self.dispatch_to_app_command_handler
        )  # Register error handler for app commands.

    async def dispatch_to_app_command_handler(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        """Dispatch command error to app_command_error event."""
        await self.on_app_command_error(interaction, error)

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        """Handle app command errors."""
        error_message = error_map.get(type(error), self.error_message).format(error=error)

        if interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)

        if type(error) not in error_map:
            self.log_error_traceback(error)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context[commands.Bot], error: commands.CommandError
    ):
        """Handle traditional command errors."""
        if isinstance(
            error,
            commands.CommandNotFound,
        ):
            return  # Ignore these specific errors.

        # Get the error message from the error_map.
        error_message = error_map.get(type(error), self.error_message).format(error=error, ctx=ctx)

        """Create an embed with the error message and send it to the user."""
        embed = discord.Embed()

        embed.color = CONST.COLORS["ERROR"]

        embed.set_author(
            name="Error",
            icon_url="https://media.discordapp.net/attachments/1223690612822376529/1224806931110301887/Error-512.png",
        )

        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/1223690612822376529/1224811009995182171/tux-294571_640.png"
        )

        embed.title = "Uh oh! An error occurred."

        embed.description = error_message

        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )

        embed.timestamp = ctx.message.created_at

        await ctx.send(embed=embed)

        if type(error) not in error_map:
            self.log_error_traceback(error)

    def log_error_traceback(self, error: Exception):
        """Helper method to log error traceback."""
        trace = traceback.format_exception(None, error, error.__traceback__)
        formatted_trace = "".join(trace)
        logger.error(f"Error: {error}\nTraceback:\n{formatted_trace}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))
