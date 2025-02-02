import contextlib
import datetime

import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from prisma.models import Reminders
from tux.database.controllers import DatabaseController
from tux.utils.embeds import EmbedCreator
from tux.utils.functions import convert_to_seconds


def get_closest_reminder(reminders: list[Reminders]) -> Reminders | None:
    """
    Check if there are any reminders and return the closest one.


    Parameters
    ----------
    reminders : list[Reminders]
        A list of reminders to check.

    Returns
    -------
    Reminders | None
        The closest reminder or None if there are no reminders.
    """
    return min(reminders, key=lambda x: x.expires_at) if reminders else None


# TODO: Refactor and clean up this code


class RemindMe(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db_controller = DatabaseController()
        self.bot.loop.create_task(self.update())

    async def send_reminders(self, reminder: Reminders) -> None:
        """
        Send the reminder to the user.

        Parameters
        ----------
        reminder : Reminders
            The reminder object.
        """

        user = self.bot.get_user(reminder.user_id)

        if user is not None:
            embed = EmbedCreator.custom_footer_embed(
                ctx=None,
                interaction=None,
                state="SUCCESS",
                user=user,
                latency="N/A",
                content=reminder.content,
                title="Reminder",
            )

            try:
                await user.send(embed=embed)

            except discord.Forbidden:
                # Send a message in the channel if the user has DMs closed
                channel: (
                    discord.abc.GuildChannel | discord.Thread | discord.abc.PrivateChannel | None
                ) = self.bot.get_channel(reminder.channel_id)

                if channel is not None and isinstance(
                    channel, discord.TextChannel | discord.Thread | discord.VoiceChannel
                ):
                    with contextlib.suppress(discord.Forbidden):
                        await channel.send(
                            content=f"{user.mention} Failed to DM you, sending in channel",
                            embed=embed,
                        )

                else:
                    logger.error(
                        f"Failed to send reminder to {user.id}, DMs closed and channel not found."
                    )

        else:
            logger.error(f"Failed to send reminder to {reminder.user_id}, user not found.")

        # Delete the reminder after sending
        await self.db_controller.reminders.delete_reminder(reminder.id)

        # Run update again to check if there are any more reminders
        await self.update()

    async def end_timer(self, reminder: Reminders) -> None:
        """
        End the timer for the reminder.

        Parameters
        ----------
        reminder : Reminders
            The reminder object.
        """

        # Wait until the reminder expires
        await discord.utils.sleep_until(reminder.expires_at)
        await self.send_reminders(reminder)

    async def update(self) -> None:
        """
        Update the reminders

        Check if there are any reminders and send the closest one.
        """

        try:
            # Get all reminders
            reminders = await self.db_controller.reminders.get_all_reminders()
            # Get the closest reminder
            closest_reminder = get_closest_reminder(reminders)

        except Exception as e:
            logger.error(f"Error getting reminders: {e}")
            return

        # If there are no reminders, return
        if closest_reminder is None:
            return

        # Check if it's expired
        if closest_reminder.expires_at < datetime.datetime.now(datetime.UTC):
            await self.send_reminders(closest_reminder)
            return

        # Create a task to wait until the reminder expires
        self.bot.loop.create_task(self.end_timer(closest_reminder))

    @app_commands.command(
        name="remindme", description="Reminds you after a certain amount of time."
    )
    async def remindme(self, interaction: discord.Interaction, time: str, *, reminder: str) -> None:
        """
        Set a reminder for a certain amount of time.

        Parameters
        ----------
        interaction : discord.Interaction
            The discord interaction object.
        time : str
            The time to wait before reminding.
        reminder : str
            The reminder message.
        """

        seconds = convert_to_seconds(time)

        # Check if the time is valid (this is set to 0 if the time is invalid via convert_to_seconds)
        if seconds == 0:
            await interaction.response.send_message(
                "Invalid time format. Please use a format like `1d`, `2h`, `3m`, etc. (only days, hours, and minutes are supported)"
            )
            return

        seconds = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=seconds)

        try:
            await self.db_controller.reminders.create_reminder(
                user_id=interaction.user.id,
                reminder_content=reminder,
                expires_at=seconds,
                channel_id=interaction.channel_id or 0,
                guild_id=interaction.guild_id or 0,
            )

            embed = EmbedCreator.create_success_embed(
                title="Reminder Set",
                description=f"Reminder set for <t:{int(seconds.timestamp())}:f>.",
                interaction=interaction,
            )

            embed.add_field(
                name="Note",
                value="If you have DMs closed, the reminder may not reach you. We will attempt to send it in this channel instead, however it is not guaranteed.",
            )

        except Exception as e:
            embed = EmbedCreator.create_error_embed(
                title="Error",
                description="There was an error creating the reminder.",
                interaction=interaction,
            )

            logger.error(f"Error creating reminder: {e}")

        await interaction.response.send_message(embed=embed)

        # Run update again to check if this reminder is the closest
        await self.update()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RemindMe(bot))
