import datetime

import discord
from discord.ext import commands

from tux.utils.constants import Constants as CONST


def get_timestamp(
    ctx: commands.Context[commands.Bot] | None, interaction: discord.Interaction | None
) -> datetime.datetime:
    if ctx and ctx.message:
        return ctx.message.created_at
    return interaction.created_at if interaction else discord.utils.utcnow()


def get_footer(
    ctx: commands.Context[commands.Bot] | None, interaction: discord.Interaction | None
) -> tuple[str, str]:
    footer = ("", "")
    if ctx:
        footer = (f"Requested by {ctx.author.display_name}", ctx.author.display_avatar.url)
    elif interaction:
        footer = (
            f"Requested by {interaction.user.display_name}",
            interaction.user.display_avatar.url,
        )
    return footer


def base_embed(
    ctx: commands.Context[commands.Bot] | None, interaction: discord.Interaction | None, state: str
) -> discord.Embed:
    embed = discord.Embed()

    embed.color = CONST.EMBED_STATE_COLORS[state]
    embed.set_author(name=state.capitalize(), icon_url=CONST.EMBED_STATE_ICONS[state])
    embed.timestamp = get_timestamp(ctx, interaction)
    footer = get_footer(ctx, interaction)
    embed.set_footer(text=footer[0], icon_url=footer[1])

    return embed


def create_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    state: str,
    title: str,
    description: str,
) -> discord.Embed:
    embed = base_embed(ctx, interaction, state)
    embed.title = title
    embed.description = description
    return embed


def create_default_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    return create_embed(ctx, interaction, "DEFAULT", title, description)


def create_info_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    return create_embed(ctx, interaction, "INFO", title, description)


def create_error_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    return create_embed(ctx, interaction, "ERROR", title, description)


def create_warning_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    return create_embed(ctx, interaction, "WARNING", title, description)


def create_success_embed(
    ctx: commands.Context[commands.Bot] | None,
    interaction: discord.Interaction | None,
    title: str,
    description: str,
) -> discord.Embed:
    return create_embed(ctx, interaction, "SUCCESS", title, description)
